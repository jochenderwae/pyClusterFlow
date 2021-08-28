import glob
import pickle
import socket

import paramiko
from scp import SCPClient
from pathlib import Path

from remoteWorker.RemoteInvoke import RemoteInvoke, RemoteRelease
from remoteWorker.RemoteInvoke import RemoteCreate

workerDispatcherInstance = None

workerFiles = [
    "setup.py",
    "Worker.py",
    "TestClass.py",
    "remoteWorker/*.py"
]

localFiles = []
for path in workerFiles:
    localFiles += glob.glob(path)
_localFiles = []
for path in localFiles:
    _localFiles.append(Path(path).resolve())
localFiles = _localFiles
print(localFiles)


def createRemote(clsName, requiredResources, *args, **kwargs):
    if not isinstance(workerDispatcherInstance, WorkerPool):
        raise AttributeError("Client needs to be started first")
    return workerDispatcherInstance.createRemote(clsName, requiredResources, *args, **kwargs)


class WorkerProxy(object):
    def __init__(self, pool, host=socket.gethostname(), port=37373):
        self.socket = None
        self.pool = pool
        self.host = host
        self.port = port
        self.ssh = None

    def _initiateSSH(self):
        if self.ssh is None:
            self.ssh = paramiko.SSHClient()
            self.ssh.connect(self.host)

    def install(self):
        self._initiateSSH()
        scp = SCPClient(self.ssh.get_transport())
        files = []
        remote_path = ""
        scp.put(files, remote_path=remote_path)

    def startWorker(self):
        self._initiateSSH()
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command("./Worker.py")
        # disown -h %1

    def openConnection(self):
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

    def createInstance(self, clsName, requiredResources, *args, **kwargs):
        remoteInvoke = RemoteCreate(clsName, requiredResources, *args, **kwargs)
        data = pickle.dumps(remoteInvoke)
        self.send(data)
        data = self.read()
        obj = pickle.loads(data)
        if obj.exception is not None:
            return None
        return self

    def call(self, method, *args, **kwargs):
        remoteInvoke = RemoteInvoke(method, args, kwargs)
        data = pickle.dumps(remoteInvoke)
        self.send(data)
        data = self.read()
        obj = pickle.loads(data)
        return obj.returnValue

    def release(self):
        if self.socket is None:
            return
        remoteInvoke = RemoteRelease()
        data = pickle.dumps(remoteInvoke)
        self.send(data)
        data = self.read()
        obj = pickle.loads(data)
        self.socket.close()
        self.socket = None
        self.pool.removeRemote(self)


class WorkerPool:
    def __init__(self, workers=[]):
        global workerDispatcherInstance
        if isinstance(workerDispatcherInstance, WorkerPool):
            raise AttributeError("WorkerPool has already been created")
        workerDispatcherInstance = self

        self.workerDefinitions = workers
        self.workers = []
        self.remoteInstances = []

    def addWorker(self, worker):
        self.workerDefinitions.append(worker)

    def start(self):
        for workerDefinition in self.workerDefinitions:
            worker = WorkerProxy(self, host=workerDefinition["host"], port=workerDefinition["port"])
            self.workers.append(worker)
            worker.openConnection()

    def stop(self):
        for instance in self.remoteInstances:
            instance.release()

    def createRemote(self, clsName, requiredResources, *args, **kwargs):
        for remoteWorker in self.workers:
            remoteInstance = remoteWorker.createInstance(clsName, requiredResources, *args, **kwargs)
            if remoteInstance is not None:
                self.remoteInstances.append(remoteInstance)
                return remoteInstance

        raise AttributeError("No matching worker found")

    def removeRemote(self, remote):
        self.remoteInstances.remove(remote)
