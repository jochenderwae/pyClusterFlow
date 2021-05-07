
import pickle

class RemoteInvoke:
    def __init__(self):
        self.class_name = None
        self.remoteInstanceId = None
        self.method = None
        self.args = None
        self.kwargs = None

class RemoteReturn:
    def __init__(self):
        self.class_name = None
        self.remoteInstanceId = None
        self.method = None
        self.returnValue = None

def SerializeData(object):
    return pickle.dumps(object)

def DeserializeData(data):
    return pickle.loads(data)

class RemoteClass:
    def __init__(self):
        self.remoteHost = ""
        self.remoteInstanceId = -1

    def doConstructor(self):
        dummy = 0

    def doInvoke(self, method, args, kwargs):
        remoteInvoke = RemoteInvoke()
        remoteInvoke.remoteInstanceId = self.remoteInstanceId
        remoteInvoke.method = method
        remoteInvoke.args = args
        remoteInvoke.kwargs = kwargs

        data = SerializeData(remoteInvoke)
        returnData = self.server.sendData(data)
        remoteReturn = DeserializeData(returnData)

        print(remoteReturn)
        return remoteReturn.returnValue