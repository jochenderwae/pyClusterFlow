from typing import Optional, Set

from adhesive.graph.Loop import Loop
from adhesive.graph.ProcessNode import ProcessNode
from adhesive.graph.time.TimerBoundaryEvent import TimerBoundaryEvent


class ProcessTask(ProcessNode):
    """
    ProcessTask is anything that has a runnable task.
    """
    def __init__(self,
                 *args,
                 id: str,
                 name: str,
                 parent_process: 'Process') -> None:
        if args:
            raise Exception("You need to use named parameters")

        super(ProcessTask, self).__init__(
            id=id,
            name=name,
            parent_process=parent_process)

        self.error_task: Optional['ErrorBoundaryEvent'] = None
        self.timer_events: Optional[Set[TimerBoundaryEvent]] = None

        self.loop: Optional[Loop] = None

    def add_timer(self, timer_boundary_event: TimerBoundaryEvent) -> None:
        if not self.timer_events:
            self.timer_events = set()

        self.timer_events.add(timer_boundary_event)

    def __str__(self) -> str:
        return f"ProcessTask({self.id}): {self.name}"

# FIXME: this import should be done, for mypy
# from adhesive.graph.BoundaryEvent import ErrorBoundaryEvent
# from adhesive.graph.Process import Process
