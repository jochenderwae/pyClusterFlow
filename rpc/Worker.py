import pickle
import threading
import socket
from importlib import import_module
from enum import Enum

from rpc.RemoteInvoke import RemoteCreate, RemoteInvoke, RemoteReturn, IllegalWorkerStateException, \
    UnknownMethodException, UnknownClassException, ResourcesNotAvailableException, RemoteRelease


class WorkerThreadState(Enum):
    CREATED = 0
    STARTED = 1
    RUNNING = 2
    ENDED = 3


def start(settingsDictionary):
    worker = Worker(settingsDictionary)
    print("starting worker")
    worker.start()
    return worker


class Worker(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, settings):
        self.serverSocket = None
        self.port = settings["port"]
        self.resources = {}
        for resourceName in settings["resources"]:
            amount = settings["resources"][resourceName]
            self.resources[resourceName] = []
            for i in range(amount):
                self.resources[resourceName].append(resourceName)
        print(self.resources)

    def start(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind(("localhost", self.port))  # socket.gethostname()
        serverSocket.listen(5)

        while True:
            (clientSocket, address) = serverSocket.accept()
            ct = WorkerThread(self, clientSocket)
            ct.run()

    def reserveResources(self, requiredResources):
        reservedResources = []
        for resourceName in requiredResources:
            if resourceName not in self.resources or len(self.resources[resourceName]) == 0:
                raise ResourcesNotAvailableException("Resource \"{}\" not available".format(resourceName))

        for resourceName in requiredResources:
            for n in range(requiredResources[resourceName]):
                reservedResources.append(self.resources[resourceName].pop())

        return reservedResources

    def releaseResources(self, reservedResources):
        if reservedResources is None:
            return
        for resourceName in reservedResources:
            self.resources[resourceName].append(resourceName)


class WorkerThread(threading.Thread):
    def __init__(self, worker, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.worker = worker
        self.className = ""
        self.instance = None
        self.reservedResources = None
        self.state = None

    def run(self):
        self.state = WorkerThreadState.CREATED
        try:
            while True:
                data = self.read()
                command = pickle.loads(data)
                response = self.handleCommand(command)

                if response is None:
                    response = RemoteReturn("constructor", None,
                                            IllegalWorkerStateException("Call resulted in an empty response"))

                data = pickle.dumps(response)
                self.send(data)

        except (RuntimeError, ConnectionResetError):
            print("socket closed")

        self.state = WorkerThreadState.ENDED
        self.worker.releaseResources(self.reservedResources)

    def handleCommand(self, command):
        try:
            if isinstance(command, RemoteCreate):
                if self.state is not WorkerThreadState.CREATED:
                    raise IllegalWorkerStateException(
                        "Worker needs to be in the state CREATED when sending a constructor. State was {} instead".format(
                            self.state))

                self.reservedResources = self.worker.reserveResources(command.requiredResources)
                self.className = command.clsName
                modulePath, className = self.className.rsplit('.', 1)
                module = import_module(modulePath)
                if module is None:
                    raise UnknownClassException("Package {} not found".format(modulePath))
                cls = getattr(module, className)
                if cls is None:
                    raise UnknownClassException("Class {} not found in package {}".format(className, modulePath))
                self.instance = cls()
                self.state = WorkerThreadState.STARTED
                return RemoteReturn("constructor", None, None)

            if isinstance(command, RemoteInvoke):
                if self.state is not WorkerThreadState.STARTED:
                    raise IllegalWorkerStateException(
                        "Worker needs to be in the state STARTED when sending a method call. State was {} instead".format(
                            self.state))
                self.state = WorkerThreadState.RUNNING
                method = getattr(self.instance, command.method)
                if method is None:
                    raise UnknownMethodException("Method {} not found in {}".format(command.method, self.className))
                returnValue = method(*command.args, **command.kwargs)
                self.state = WorkerThreadState.STARTED
                return RemoteReturn(command.method, returnValue, None)

            if isinstance(command, RemoteRelease):
                if self.state is not WorkerThreadState.STARTED and self.state is not WorkerThreadState.CREATED:
                    raise IllegalWorkerStateException(
                        "Worker needs to be in the state STARTED or CREATED when sending a remote release. State was {} instead".format(
                            self.state))

                # instance destructor?
                self.instance = None
                self.state = WorkerThreadState.ENDED
                self.worker.releaseResources(self.reservedResources)
                self.className = ""
                return RemoteReturn("release", None, None)

        except BaseException as e:
            return RemoteReturn("constructor", None, e)

        return None

    def send(self, msg):
        sent = self.clientSocket.send(msg)
        if sent == 0:
            raise RuntimeError("socket connection broken")

    def read(self):
        data = self.clientSocket.recv(2048)
        if data == b'':
            raise RuntimeError("socket connection broken")
        return data
