from typing import Optional, Dict, Any, Generic, TypeVar, cast

from adhesive.execution import token_utils
from adhesive.execution.ExecutionData import ExecutionData
from adhesive.graph.ExecutableNode import ExecutableNode

T = TypeVar('T')


class ExecutionToken(Generic[T]):
    """
    A context passed to an execution of a task. It holds the information
    about:
    - data that's attached to this token,
    - loop information (when in a loop).

    A process context it's an execution token that's being passed around.
    """
    def __init__(self,
                 *,
                 task: ExecutableNode,
                 execution_id: str,
                 token_id: str,
                 data: Optional[Dict]) -> None:
        self.task = task
        self.data: T = cast(T, ExecutionData(data))
        self.execution_id = execution_id
        self.token_id = token_id

        # we need to define it before calling token_utils.parse_name. That's
        # since parse_name() will read this object using as_mapping(), that in
        # turn reads the task_name
        self.task_name = ""

        self.loop: Optional[ExecutionLoop] = None

    def _update_title_from_data(self) -> None:
        self.task_name = token_utils.parse_name(self, self.task.name)

    def clone(self, task: ExecutableNode) -> 'ExecutionToken[T]':
        result: ExecutionToken[T] = ExecutionToken(
            task=task,
            execution_id=self.execution_id,
            token_id=self.token_id,   # FIXME: probably a new token?
            data=cast(ExecutionData, self.data).as_dict()
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
            "context": self,
        }


from adhesive.execution.ExecutionLoop import ExecutionLoop
