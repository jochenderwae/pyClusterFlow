from remoteWorker import RemoteProxy


@RemoteProxy.remote(resources={"cpu": 1})
class ParallelTask(object):

    @RemoteProxy.method
    def execute(self):
        return "Parallel task executed"
