import pickle
import threading
import socket
from importlib import import_module

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
        # create an INET, STREAMing socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        serversocket.bind(("localhost", 37373)) # socket.gethostname()
        # become a server socket
        serversocket.listen(5)

        while True:
            # accept connections from outside
            print("accepting client sockets")
            (clientsocket, address) = serversocket.accept()
            # now do something with the clientsocket
            # in this case, we'll pretend this is a threaded server
            ct = WorkerThread(clientsocket)
            ct.run()

class WorkerThread (threading.Thread):
    def __init__(self, clientsocket):
        threading.Thread.__init__(self)
        self.clientsocket = clientsocket
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
                    print("Received create class: {} {}".format(self.nextObjectId, instance))
                    response = RemoteReturn(self.nextObjectId, "constructor", None)
                    self.nextObjectId += 1

#except (ImportError, AttributeError) as e:
#    raise ImportError(command.clsName)

                if isinstance(command, RemoteInvoke):
                    instance = self.objectCache[command.remoteInstanceId]
                    method = getattr(instance, command.method)
                    returnValue = method(instance, command.args, command.kwargs)
                    print("Received method call {} on instance {}".format(command.method, command.remoteInstanceId))
                    response = RemoteReturn(command.remoteInstanceId, command.method, returnValue)

                if response is not None:
                    data = pickle.dumps(response)
                    self.send(data)
        except RuntimeError:
            print("socket closed")

    def send(self, msg):
        sent = self.clientsocket.send(msg)
        if sent == 0:
            raise RuntimeError("socket connection broken")

    def read(self):
        data = self.clientsocket.recv(2048)
        if data == b'':
            raise RuntimeError("socket connection broken")
        return data

