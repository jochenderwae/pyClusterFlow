from remoteWorker import RemoteProxy
from remoteWorker.RemoteProxy import is_worker


@RemoteProxy.remote(resources={"cpu": 1})
class ParallelTask(object):

    @RemoteProxy.method
    def execute(self, _dict):
        return "Parallel task executed. Is worker: {} - count: {}".format(is_worker, _dict["count"])


