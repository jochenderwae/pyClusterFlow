import socket

from remoteWorker import WorkerDispatcher
from remoteWorker.WorkerDispatcher import WorkerPool
from testApplication.ParallelTask import ParallelTask

if __name__ == '__main__':

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

    #https://bpmn.io/

    from adhesive import config
    config.current.parallel_processing = 'thread'
    import testApplication.main

    pool.stop()
