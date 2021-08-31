import socket

from remoteWorker import WorkerDispatcher
from TestClass import TestClass
from remoteWorker.WorkerDispatcher import WorkerPool


hostname = socket.gethostname()
hostname = "localhost"

workers = [
    #{"host": "piworker1", "port": 37373},
    {"host": hostname, "port": 37373},
    {"host": hostname, "port": 37374},
    #    {"host": hostname, "port": 37375},
    #    {"host": hostname, "port": 37376},
]
pool = WorkerPool(workers=workers)
# pool.addWorker({"host": hostname, "port": 37377})

workers = pool.getWorkers()
#workers[0].install()
#workers[0].startWorker()
#pool.start()
'''
test = TestClass()
response = test.remote_method(1)
print("remote_method (1) returned: {}".format(response))
response = test.remote_method("Two")
print("remote_method (2) returned: {}".format(response))
response = test.remote_method("3")
print("remote_method (3) returned: {}".format(response))
try:
    test.local_method()
except AttributeError:
    pass

test = None
'''
import testApplication.main

pool.stop()
