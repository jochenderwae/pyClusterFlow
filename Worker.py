import os
import sys
import json

from remoteWorker import Worker
from remoteWorker import RemoteProxy

RemoteProxy.is_worker = True

settings = {
    "resources": {
        "cpu": 2
    },
    "port": 37373
}
if len(sys.argv) > 1:
    file = open(sys.argv[1], "r")
    settings = json.load(file)
    file.close()

Worker.start(settings)


