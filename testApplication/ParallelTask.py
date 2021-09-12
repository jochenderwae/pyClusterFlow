from remoteWorker import RemoteProxy
from remoteWorker.RemoteProxy import is_worker, RemoteTask


class ParallelTask(RemoteTask):

    def execute(self, data):
        data["ParallelTask_data"].append("Parallel task executed. Is worker: {} - count: {}".format(is_worker, data["count"]))
        return data


class RepetitiveTask(RemoteTask):
    def execute(self, data):
        data["RepetitiveTask"] = "Task is done"
        return data
