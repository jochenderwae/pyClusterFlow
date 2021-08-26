from rpc import WorkerDispatcher
from TestClass import TestClass

WorkerDispatcher.start()


test = TestClass()
response = test.remote_method()
print("remote_method returned: {}".format(response))
try:
    test.local_method()
except AttributeError:
    pass
