
import pickle

class RemoteCreate:
    def __init__(self, clsName, *args, **kwargs):
        self.clsName = clsName
        self.args = args
        self.kwargs = kwargs

class RemoteInvoke:
    def __init__(self, remoteInstanceId, method, args, kwargs):
        self.remoteInstanceId = remoteInstanceId
        self.method = method
        self.args = args
        self.kwargs = kwargs

class RemoteReturn:
    def __init__(self, remoteInstanceId, method, returnValue):
        self.remoteInstanceId = remoteInstanceId
        self.method = method
        self.returnValue = returnValue
