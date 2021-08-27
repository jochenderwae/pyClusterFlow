import pickle
import socket

from rpc.RemoteInvoke import RemoteInvoke
from rpc.RemoteInvoke import RemoteCreate

workerDispatcherInstance = None


def createRemote(clsName, requiredResources, *args, **kwargs):
    if not isinstance(workerDispatcherInstance, WorkerPool):
        raise AttributeError("Client needs to be started first")
    return workerDispatcherInstance.createRemote(clsName, requiredResources, *args, **kwargs)


class WorkerProxy(object):

    def __init__(self, host=socket.gethostname(), port=37373):
        self.socket = None
        self.host = host
        self.port = port

    def startClient(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("connecting to {}:{}".format(self.host, self.port))
        self.socket.connect((self.host, self.port))

    def send(self, msg):
        sent = self.socket.send(msg)
        if sent == 0:
            raise RuntimeError("socket connection broken")

    def read(self):
        data = self.socket.recv(2048)
        if data == b'':
            raise RuntimeError("socket connection broken")
        return data

    def createRemote(self, clsName, requiredResources, *args, **kwargs):
        remoteInvoke = RemoteCreate(clsName, requiredResources, *args, **kwargs)
        data = pickle.dumps(remoteInvoke)
        self.send(data)
        data = self.read()
        obj = pickle.loads(data)
        if obj.exception is not None:
            return None
        remote = RemoteClass(self)
        return remote


class RemoteClass:
    def __init__(self, client):
        self.client = client

    def call(self, method, *args, **kwargs):
        remoteInvoke = RemoteInvoke(method, args, kwargs)
        data = pickle.dumps(remoteInvoke)
        self.client.send(data)
        data = self.client.read()
        obj = pickle.loads(data)
        return obj.returnValue


class WorkerPool:
    def __init__(self, workers=[]):
        global workerDispatcherInstance
        if isinstance(workerDispatcherInstance, WorkerPool):
            raise AttributeError("WorkerPool has already been created")
        self.workerDefinitions = workers
        self.workers = []
        workerDispatcherInstance = self

    def addWorker(self, worker):
        self.workerDefinitions.append(worker)

    def start(self):
        for workerDefinition in self.workerDefinitions:
            worker = WorkerProxy(host=workerDefinition["host"], port=workerDefinition["port"])
            self.workers.append(worker)
            worker.startClient()

    def createRemote(self, clsName, requiredResources, *args, **kwargs):
        for remoteWorker in self.workers:
            remoteInstance = remoteWorker.createRemote(clsName, requiredResources, *args, **kwargs)
            if remoteInstance is not None:
                return remoteInstance

        raise AttributeError("No matching worker found")
