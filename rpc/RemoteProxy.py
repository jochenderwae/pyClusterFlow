import functools
import inspect

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
        self.remoteInstanceId = None

    def __getattr__(self, method):
        fn = self.ctor.__dict__[method]
        if fn is None:
            return None
        if fn is remote_method:
            def remote_caller(*args, **kwargs):
                self.do_remote(method, *args, **kwargs)
            return remote_caller
        raise AttributeError("{} is not a remotely accessible method in {}".format(method, self.ctor.__name__))

    def do_remote(self, method_name, *args, **kwargs):
        print("do remote call {}({},{})".format(method_name, args, kwargs))

    def __call__(self, *args, **kwargs):
        self.do_remote("constructor", *args, **kwargs)
        return self


def remote_method(self):
    pass


@remote
class TestClass(object):

    @method
    def remote_method(self):
        print("remote_method")

    def local_method(self):
        print("you can only get here through another methond")


test = TestClass()
test.remote_method()
#test.local_method()
