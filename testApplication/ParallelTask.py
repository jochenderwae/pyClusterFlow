from remoteWorker import RemoteProxy
from remoteWorker.RemoteProxy import is_worker


@RemoteProxy.remote(resources={"cpu": 1})
class ParallelTask(object):

    @RemoteProxy.method
    def execute(self):
        return "Parallel task executed. Is worker: {}".format(is_worker)


