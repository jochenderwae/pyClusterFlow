import functools
import inspect

from rpc import WorkerDispatcher

is_worker = False


def remote(ctor, resources={"tpu": 1}):
    if is_worker:
        return ctor
    return RemoteProxy(ctor, resources)


def method(fn):
    if is_worker:
        return fn
    return remote_method


class RemoteProxy(object):

    def __init__(self, ctor, requiredResources, *args, **kwargs):
        self.ctor = ctor
        self.args = args
        self.kwargs = kwargs
        self.remoteInstanceHandle = None
        self.requiredResources = requiredResources

    def __getattr__(self, method):
        fn = self.ctor.__dict__[method]
        if fn is None:
            return None
        if fn is remote_method:
            def remote_caller(*args, **kwargs):
                if self.remoteInstanceHandle is None:
                    raise AttributeError("Constructor needs to be called")
                return self.remoteInstanceHandle.call(method, *args, **kwargs)
            return remote_caller
        raise AttributeError("{} is not a remotely accessible method in {}".format(method, self.ctor.__name__))

    def __call__(self, *args, **kwargs):
        clsName = ""
        klass = self.ctor
        module = klass.__module__
        if module == 'builtins':
            clsName = klass.__qualname__
        else:
            clsName = module + '.' + klass.__qualname__

        self.remoteInstanceHandle = WorkerDispatcher.createRemote(clsName, self.requiredResources, *args, **kwargs)
        return self

    def __del__(self):
        if self.remoteInstanceHandle is not None:
            self.remoteInstanceHandle.release()
        self.remoteInstanceHandle = None

def remote_method(self):
    pass



