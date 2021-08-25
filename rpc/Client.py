import pickle
import socket

from rpc.RemoteInvoke import RemoteInvoke
from rpc.RemoteInvoke import RemoteCreate


def start(*args, **kwargs):
    client = Client(*args, **kwargs)
    client.startClient()
    return client

def createRemote(clsName, *args, **kwargs):
    if not isinstance(Client._instance, Client):
        raise AttributeError("Client needs to be started first")
    return Client._instance.createRemote(clsName, args, kwargs)

def doRemote(method_name, args, kwargs):
    if not isinstance(Client._instance, Client):
        raise AttributeError("Client needs to be started first")
    Client._instance.doRemote(method_name, args, kwargs)

class Client(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *args, **kwargs):
        self.socket = None

    def startClient(self):
        # create an INET, STREAMing socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # now connect to the web server on port 80 - the normal http port
        self.socket.connect(("localhost", 37373))

    def doRemote(self, method_name, args, kwargs):
        if method_name == "constructor":
            #RemoteClass
            pass
        self.send(method_name.encode())
        print("Message \"{}\" sent".format(method_name))


    def send(self, msg):
        sent = self.socket.send(msg)
        if sent == 0:
            raise RuntimeError("socket connection broken")

    def read(self):
        data = self.socket.recv(2048)
        if data == b'':
            raise RuntimeError("socket connection broken")
        return data

    def createRemote(self, clsName, *args, **kwargs):
        remoteInvoke = RemoteCreate(clsName, *args, **kwargs)
        data = pickle.dumps(remoteInvoke)
        self.send(data)
        data = self.read()
        obj = pickle.loads(data)
        remote = RemoteClass(self, obj)
        return remote


class RemoteClass:
    def __init__(self, client, remoteReturn):
        self.client = client
        self.remoteInstanceId = remoteReturn.remoteInstanceId

    def call(self, method, *args, **kwargs):
        remoteInvoke = RemoteInvoke(self.remoteInstanceId, method, args, kwargs)
        data = pickle.dumps(remoteInvoke)
        self.client.send(data)
        data = self.client.read()
        obj = pickle.loads(data)
        return obj.returnValue


