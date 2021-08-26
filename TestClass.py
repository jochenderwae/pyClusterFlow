from rpc import RemoteProxy


@RemoteProxy.remote
class TestClass(object):

    @RemoteProxy.method
    def remote_method(self):
        print("remote_method, self: {}".format(self))
        return "Method called correctly"

    def local_method(self):
        print("you can only get here through another method")


