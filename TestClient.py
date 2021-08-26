import socket

from rpc import WorkerDispatcher
from TestClass import TestClass
from rpc.WorkerDispatcher import WorkerPool

hostname = socket.gethostname()
hostname = "localhost"

workers = [
    {"host": hostname, "port": 37373},
    {"host": hostname, "port": 37374}
#    {"host": hostname, "port": 37375},
#    {"host": hostname, "port": 37376}
]
pool = WorkerPool(workers=workers)
#pool.addWorker({"host": hostname, "port": 37377})
pool.start()


test = TestClass()
response = test.remote_method()
print("remote_method returned: {}".format(response))
try:
    test.local_method()
except AttributeError:
    pass
