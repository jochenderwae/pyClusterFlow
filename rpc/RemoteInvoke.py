
import pickle

class RemoteCreate:
    def __init__(self, clsName, requiredResources, *args, **kwargs):
        self.clsName = clsName
        self.requiredResources = requiredResources
        self.args = args
        self.kwargs = kwargs

class RemoteInvoke:
    def __init__(self, remoteInstanceId, method, args, kwargs):
        self.remoteInstanceId = remoteInstanceId
        self.method = method
        self.args = args
        self.kwargs = kwargs

class RemoteReturn:
    def __init__(self, remoteInstanceId, method, returnValue, exception):
        self.remoteInstanceId = remoteInstanceId
        self.method = method
        self.returnValue = returnValue
        self.exception = exception
