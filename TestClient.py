from rpc import Client
from TestClass import TestClass

Client.start()


test = TestClass()
test.remote_method()
try:
    test.local_method()
except AttributeError:
    pass
