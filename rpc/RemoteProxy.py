import functools
import inspect

is_worker = False

def Remote(ctor):
    if is_worker:
        return ctor
    return RemoteProxy(ctor)

def Method(fn):
    return fn

class RemoteProxy(object):

    def __init__(self, ctor, *args, **kwargs):
        self.ctor = ctor
        self.args = args
        self.kwargs = kwargs

    def __getattr__(self, method):
        fn = self.ctor.__dict__[method]
        if fn is None:
            raise AttributeError("{} is not a remotely accessible method in {}".format(method, self.ctor.__name__))
        print(fn.__name__)
        print(fn)
        def RemoteCaller(*args, **kwargs):
            self.do_remote(method, *args, **kwargs)
        return RemoteCaller

    def do_remote(self, method_name, *args, **kwargs):
        print("do remote call {}({},{})".format(method_name, args, kwargs))

    def __call__(self, *args, **kwargs):
        self.do_remote("constructor", *args, **kwargs)
        return self
#    def __call__(self, *args, **kwargs):
#        # instead of making the instance locally, do this remotely
#        self.remote_instance = self.constructor(*args, **kwargs)


#        members = self.constructor.__dict__
#        for item in members:
#            if type(members[item]) == RemoteProxy.Method:
#                members[item].remote_proxy = self
#                self.exposed_methods[item] = members[item]

#        return self



@Remote
class TestClass(object):

    @Method
    def remote_method(self):
        print("remote_method")

    def local_method(self):
        print("you can only get here through another methond")



test = TestClass()
test.remote_method()
test.local_method()
