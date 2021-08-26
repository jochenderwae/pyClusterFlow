from rpc import WorkerDispatcher
from TestClass import TestClass

WorkerDispatcher.start()


test = TestClass()
test.remote_method()
try:
    test.local_method()
except AttributeError:
    pass
