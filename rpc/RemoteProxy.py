import functools
import inspect

from rpc import WorkerDispatcher

is_worker = False


def remote(ctor):
    if is_worker:
        return ctor
    return RemoteProxy(ctor)


def method(fn):
    if is_worker:
        return fn
    return remote_method


class RemoteProxy(object):

    def __init__(self, ctor, *args, **kwargs):
        self.ctor = ctor
        self.args = args
        self.kwargs = kwargs
        self.remoteInstanceHandle = None

    def __getattr__(self, method):
        print("method call")
        fn = self.ctor.__dict__[method]
        if fn is None:
            return None
        if fn is remote_method:
            def remote_caller(*args, **kwargs):
                if self.remoteInstanceHandle is None:
                    raise AttributeError("Constructor needs to be called")
                self.remoteInstanceHandle.call(method, *args, **kwargs)
            return remote_caller
        raise AttributeError("{} is not a remotely accessible method in {}".format(method, self.ctor.__name__))

    def __call__(self, *args, **kwargs):
        print("Call constructor")
        clsName = ""

        klass = self.ctor
        module = klass.__module__
        if module == 'builtins':
            clsName = klass.__qualname__
        else:
            clsName = module + '.' + klass.__qualname__

        self.remoteInstanceHandle = WorkerDispatcher.createRemote(clsName, *args, **kwargs)
        print(self.remoteInstanceHandle)
        return self


def remote_method(self):
    pass



