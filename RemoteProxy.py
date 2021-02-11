import functools
import inspect


class RemoteProxy(object):
    class Method(object):
        def __init__(self, fn):
            functools.update_wrapper(self, fn)
            self.fn = fn
            self.remoteProxy = None

        def __call__(self, *args, **kwargs):
            return self.remoteProxy.doRemote("testMethod", *args, **kwargs)

    def __init__(self, constructor):
        self.constructor = constructor
        self.remoteInstance = None
        self.exposedMethods = dict()

    def __getattr__(self, method):
        if method in self.exposedMethods:
            return self.exposedMethods[method]
        else:
            raise AttributeError("{} is not a remotely accessible method in {}".format(method, self.constructor.__name__))

    def doRemote(self, methodName, *args, **kwargs):
        fn = getattr(self.remoteInstance, methodName)
        if not fn is None:
            fn(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        # instead of making the instance locally, do this remotely
        self.remoteInstance = self.constructor(*args, **kwargs)

        members = self.constructor.__dict__
        for item in members:
            if type(members[item]) == RemoteProxy.Method:
                members[item].remoteProxy = self
                self.exposedMethods[item] = members[item]

        return self



@RemoteProxy
class TestClass(object):

    @RemoteProxy.Method
    def remoteMethod(self):
        print("here");

    def localMethod(self):
        print("you can only get here through another methond")

    def testMethod(self):
        print("this is a test")


test = TestClass()
test.remoteMethod()
test.localMethod()
