import pickle
import threading
import socket

from rpc.RemoteInvoke import RemoteCreate, RemoteInvoke, RemoteReturn


def start(*args, **kwargs):
    server = Server(*args, **kwargs)
    print("starting server")
    server.startServer()
    return server


class Server(object):
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
            ct = ServerThread(clientsocket)
            ct.run()

class ServerThread (threading.Thread):
    def __init__(self, clientsocket):
        threading.Thread.__init__(self)
        self.clientsocket = clientsocket
        self.objectId = 0

    def run(self):
        try:
            while True:
                data = self.read()
                command = pickle.loads(data)
                if isinstance(command, RemoteCreate):
                    print("Received create class: {}".format(self.objectId))
                    response = RemoteReturn(self.objectId, "constructor", None)
                    self.objectId += 1
                if isinstance(command, RemoteInvoke):
                    print("Received method call {} on instance {}".format(command.method, command.remoteInstanceId))
                    response = RemoteReturn(command.remoteInstanceId, command.method, None)
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

