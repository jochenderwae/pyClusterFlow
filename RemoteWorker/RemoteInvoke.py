import pickle


class RemoteException(Exception):
    pass


class IllegalWorkerStateException(RemoteException):
    pass


class UnknownClassException(RemoteException):
    pass


class UnknownMethodException(RemoteException):
    pass


class ResourcesNotAvailableException(RemoteException):
    pass


class RemoteCreate:
    def __init__(self, clsName, requiredResources, *args, **kwargs):
        self.clsName = clsName
        self.requiredResources = requiredResources
        self.args = args
        self.kwargs = kwargs


class RemoteInvoke:
    def __init__(self, method, args, kwargs):
        self.method = method
        self.args = args
        self.kwargs = kwargs


class RemoteRelease:
    def __init__(self):
        pass


class RemoteReturn:
    def __init__(self, method, returnValue, exception=None):
        self.method = method
        self.returnValue = returnValue
        self.exception = exception
