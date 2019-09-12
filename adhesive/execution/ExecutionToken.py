from typing import Optional, Dict, Any

from adhesive.graph.BaseTask import BaseTask
from adhesive.execution.ExecutionData import ExecutionData
from adhesive.workspace.Workspace import Workspace
from adhesive.execution import token_utils

from .ExecutionLaneId import ExecutionLaneId


class ExecutionToken:
    """
    A context passed to an execution of a task. It holds the information
    about:
    - data that's attached to this token,
    - workspace where files can be created. This depends on the actual runtime
      (ie linux, windows, docker)
    - loop information (when in a loop).

    A process context it's an execution token that's being passed around.
    """
    def __init__(self,
                 *args,
                 task: 'BaseTask',
                 execution_id: str,
                 token_id: str,
                 data: Optional[Dict],
                 workspace: Optional[Workspace] = None) -> None:
        if args:
            raise Exception("You need to pass the parameters by name")

        self.task = task
        self.data = ExecutionData(data)
        self.execution_id = execution_id
        self.token_id = token_id
        self.task_name: Optional[str] = None

        # These are None until the task is assgined to a lane
        self.workspace: Optional[Workspace] = workspace
        self.lane: Optional[ExecutionLaneId] = None

        self.loop: Optional[ExecutionLoop] = None
        self.task_name = token_utils.parse_name(self, self.task.name)

    def clone(self, task: 'BaseTask') -> 'ExecutionToken':
        result = ExecutionToken(
            task=task,
            execution_id=self.execution_id,
            token_id=self.token_id,   # FIXME: probably a new token?
            data=self.data.as_dict(),
            workspace=self.workspace.clone() if self.workspace else None,
        )

        return result

    def as_mapping(self) -> Dict[str, Any]:
        """
        This mapping is for evaluating routing conditions.
        :return:
        """
        return {
            "task": self.task,
            "execution_id": self.execution_id,
            "token_id": self.token_id,
            "data": self.data,
            "loop": self.loop,
            "task_name": self.task_name,
            "lane": self.lane,
            "context": self,
        }


from adhesive.execution.ExecutionLoop import ExecutionLoop

