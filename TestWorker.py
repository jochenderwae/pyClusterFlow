from rpc import Worker
from rpc import RemoteProxy
RemoteProxy.is_worker = True

from TestClass import TestClass

Worker.start()


