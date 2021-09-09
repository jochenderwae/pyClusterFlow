import abc
import functools
import inspect
from typing import Optional, Union, List

import adhesive
from adhesive import ExecutionTask, AdhesiveProcess, ExecutionToken
from adhesive.execution import token_utils
from adhesive.execution.ExecutionBaseTask import ExecutionBaseTask
from adhesive.logredirect.LogRedirect import redirect_stdout
from adhesive.model.ActiveEvent import ActiveEvent
from remoteWorker import WorkerDispatcher

is_worker = False


def remote(resources):
    def decorator(ctor):
        if is_worker:
            return ctor
        return RemoteProxy(ctor, resources)

    return decorator


def method(fn):
    if is_worker:
        return fn
    return remote_method


class RemoteProxy(object):

    def __init__(self, ctor, requiredResources, *args, **kwargs):
        self.ctor = ctor
        self.args = args
        self.kwargs = kwargs
        self.remoteInstanceHandle = None
        self.requiredResources = requiredResources

    def __getattr__(self, method):
        fn = self.ctor.__dict__[method]
        if fn is None:
            return None
        if fn is remote_method:
            def remote_caller(*args, **kwargs):
                if self.remoteInstanceHandle is None:
                    raise AttributeError("Constructor needs to be called")
                return self.remoteInstanceHandle.call(method, *args, **kwargs)

            return remote_caller
        raise AttributeError("{} is not a remotely accessible method in {}".format(method, self.ctor.__name__))

    def __call__(self, *args, **kwargs):
        clsName = ""
        klass = self.ctor
        module = klass.__module__
        if module == 'builtins':
            clsName = klass.__qualname__
        else:
            clsName = module + '.' + klass.__qualname__

        self.remoteInstanceHandle = WorkerDispatcher.createRemote(clsName, self.requiredResources, *args, **kwargs)
        return self

    def __del__(self):
        if self.remoteInstanceHandle is not None:
            self.remoteInstanceHandle.release()
        self.remoteInstanceHandle = None


def remote_method(self):
    pass


class RemoteTask:
    __metaclass__ = abc.ABCMeta

    class AdhesiveTask(ExecutionBaseTask):
        def __init__(self, *task_names: str,
                     re: Optional[Union[str, List[str]]] = None,
                     loop: Optional[str] = None,
                     when: Optional[str] = None,
                     deduplicate: Optional[str] = None,
                     remoteInstance=None):
            super().__init__(expressions=task_names,
                             regex_expressions=re,
                             deduplicate=deduplicate,
                             code=None
                             )
            self.loop = loop
            self.when = when
            self.remoteInstance = remoteInstance

        def invoke(self, event: ActiveEvent) -> ExecutionToken:
            with redirect_stdout(event):
                params = token_utils.matches(self.re_expressions, event.context.task_name)

                returnValue = self.remoteInstance.invoke(event.context.data.as_dict())
                # TODO: do something with this return value

                return event.context


    @classmethod
    def bindToDefinition(cls, *task_names: str,
                         re: Optional[Union[str, List[str]]] = None,
                         loop: Optional[str] = None,
                         when: Optional[str] = None,
                         deduplicate: Optional[str] = None):

        clsName = ""
        module = cls.__module__
        if module == 'builtins':
            clsName = cls.__qualname__
        else:
            clsName = module + '.' + cls.__qualname__

        remoteInstanceHandle = WorkerDispatcher.createRemote(clsName, cls.getRequiredResources())

        remoteInstance = cls(remoteInstanceHandle)
        task = RemoteTask.AdhesiveTask(*task_names, re=re, loop=loop, when=when, deduplicate=deduplicate, remoteInstance=remoteInstance)
        adhesive.process.task_definitions.append(task)
        adhesive.process.chained_task_definitions.append(task)

    def __init__(self, remoteInstanceHandle=None):
        self.remoteInstanceHandle = remoteInstanceHandle

    def invoke(self, data):
        return self.remoteInstance.call("execute", data)

    @abc.abstractmethod
    def execute(self, data):
        """Method documentation"""
        return

    @classmethod
    @abc.abstractmethod
    def getRequiredResources(self):
        return {"cpu": 1}

    def __repr__(self) -> str:
        return f"@task(expressions={self.expressions}, class={self.__class__.__name__})"
