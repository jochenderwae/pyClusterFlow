import glob
import pickle
import socket

import paramiko
from scp import SCPClient
from pathlib import Path

from remoteWorker.RemoteInvoke import RemoteInvoke, RemoteRelease
from remoteWorker.RemoteInvoke import RemoteCreate

workerDispatcherInstance = None


def createRemote(clsName, requiredResources, *args, **kwargs):
    if not isinstance(workerDispatcherInstance, WorkerPool):
        raise AttributeError("Client needs to be started first")
    return workerDispatcherInstance.createRemote(clsName, requiredResources, *args, **kwargs)


class FileSet:
    workerFiles = [
        "workerSetup.sh",
        "setup.py",
        "Worker.py",
        "TestClass.py",
        "remoteWorker/*.py"
    ]

    def __init__(self, workingDirectory, hostname):
        self.fileList = FileSet.workerFiles
        self.hostname = hostname
        self.workingDirectory = workingDirectory
        self._addConfigurationFile()
        self._expandWildcards()
        self._resolveFiles()

    def getFileList(self):
        return self.fileList

    def _expandWildcards(self):
        expandedFiles = []
        for path in self.fileList:
            expandedFiles += glob.glob(path)
        self.fileList = expandedFiles
        return self

    def _resolveFiles(self):
        resolvedFiles = []
        for path in self.fileList:
            localFile = Path(path).resolve()
            remoteFile = (Path(self.workingDirectory) / path).resolve()
            resolvedFiles.append((localFile, remoteFile))
        self.fileList = resolvedFiles
        return self

    def _addConfigurationFile(self):
        configFile = self.hostname + ".Config.json"
        self.fileList.append(configFile)
        return self

    def __repr__(self):
        return self.fileList.__repr__()

    def __str__(self):
        return self.fileList.__str__()


class WorkerProxy(object):
    def __init__(self, pool, host=socket.gethostname(), port=37373):
        self.socket = None
        self.pool = pool
        self.host = host
        self.port = port
        self.ssh = None
        self.workingDirectory = "/srv/worker"

    def _initiateSSH(self):
        if self.ssh is None:
            self.ssh = paramiko.SSHClient()
            self.ssh.load_system_host_keys()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.host)

    def install(self):
        fileSet = FileSet(self.workingDirectory, self.host)
        self._initiateSSH()

        directories = []
        for (localPath, remotePath) in fileSet.getFileList():
            directories.append(remotePath.parent)
        directories = list(set(directories))

        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command("sudo mkdir -p {}".format(self.workingDirectory))
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command("sudo chmod a+rwx {}".format(self.workingDirectory))
        for directory in directories:
            print("mkdir -p {}".format(str(directory)))
            ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command("mkdir -p {}".format(str(directory)))
            for line in iter(ssh_stderr.readline, ""):
                print(line, end="")

        scp = SCPClient(self.ssh.get_transport())
        for (localPath, remotePath) in fileSet.getFileList():
            scp.put(localPath, remote_path=str(remotePath))

    def startWorker(self):
        self._initiateSSH()
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command("cd {} && bash workerSetup.sh".format(self.workingDirectory))
        for line in iter(ssh_stderr.readline, ""):
            print(line, end="")
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command("cd {} && python3 Worker.py".format(self.workingDirectory))#, get_pty=True)
        for line in iter(ssh_stderr.readline, ""):
            print(line, end="")

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

    def getWorkers(self):
        return self.workers

    def addWorker(self, worker):
        self.workerDefinitions.append(worker)

    def start(self):
        for workerDefinition in self.workerDefinitions:
            worker = WorkerProxy(self, host=workerDefinition["host"], port=workerDefinition["port"])
            self.workers.append(worker)
            #worker.openConnection()

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
