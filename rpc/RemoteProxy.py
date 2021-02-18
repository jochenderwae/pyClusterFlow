import functools
import inspect

is_worker = False

class RemoteProxy(object):
    @staticmethod
    def SetWorker(_is_worker = True):
        is_worker = _is_worker

    @staticmethod
    def IsWorker():
        return is_worker

    class Method(object):
        def __init__(self, fn):
            functools.update_wrapper(self, fn)
            self.fn = fn
            self.remote_proxy = None

        def __call__(self, *args, **kwargs):
            if(is_worker):
                return self.fn
            else:
                return self.remote_proxy.do_remote(self.fn.__name__, *args, **kwargs)

    def __init__(self, constructor):
        self.constructor = constructor
        self.remote_instance = None
        self.exposed_methods = dict()

    def __getattr__(self, method):
        if method in self.exposed_methods:
            return self.exposed_methods[method]
        else:
            raise AttributeError("{} is not a remotely accessible method in {}".format(method, self.constructor.__name__))

    def do_remote(self, method_name, *args, **kwargs):
        fn = getattr(self.remote_instance, method_name).fn
        if not fn is None:
            fn(self.remote_instance, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        # instead of making the instance locally, do this remotely
        self.remote_instance = self.constructor(*args, **kwargs)

        members = self.constructor.__dict__
        for item in members:
            if type(members[item]) == RemoteProxy.Method:
                members[item].remote_proxy = self
                self.exposed_methods[item] = members[item]

        return self



@RemoteProxy
class TestClass(object):

    @RemoteProxy.Method
    def remote_method(self):
        print("remote_method")

    def local_method(self):
        print("you can only get here through another methond")



test = TestClass()
test.remote_method()
test.local_method()
