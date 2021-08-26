import pickle
import threading
import socket
from importlib import import_module

import rpc.RemoteProxy
from rpc.RemoteInvoke import RemoteCreate, RemoteInvoke, RemoteReturn


def start(*args, **kwargs):
    server = Worker(*args, **kwargs)
    print("starting server")
    server.startServer()
    return server


class Worker(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *args, **kwargs):
        self.serversocket = None


    def startServer(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(("localhost", 37373))
        serversocket.listen(5)

        while True:
            (clientSocket, address) = serversocket.accept()
            ct = WorkerThread(clientSocket)
            ct.run()

class WorkerThread (threading.Thread):
    def __init__(self, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.nextObjectId = 0
        self.objectCache = {}

    def run(self):
        try:
            while True:
                data = self.read()
                command = pickle.loads(data)
                response = None

                if isinstance(command, RemoteCreate):
#try:
                    module_path, class_name = command.clsName.rsplit('.', 1)
                    module = import_module(module_path)
                    cls = getattr(module, class_name)
                    instance = cls()
                    self.objectCache[self.nextObjectId] = instance
                    response = RemoteReturn(self.nextObjectId, "constructor", None)
                    self.nextObjectId += 1

#except (ImportError, AttributeError) as e:
#    raise ImportError(command.clsName)

                if isinstance(command, RemoteInvoke):
                    instance = self.objectCache[command.remoteInstanceId]
                    method = getattr(instance, command.method)
                    returnValue = method(*command.args, **command.kwargs)
                    response = RemoteReturn(command.remoteInstanceId, command.method, returnValue)

                if response is not None:
                    data = pickle.dumps(response)
                    self.send(data)
        except RuntimeError:
            print("socket closed")

    def send(self, msg):
        sent = self.clientSocket.send(msg)
        if sent == 0:
            raise RuntimeError("socket connection broken")

    def read(self):
        data = self.clientSocket.recv(2048)
        if data == b'':
            raise RuntimeError("socket connection broken")
        return data


