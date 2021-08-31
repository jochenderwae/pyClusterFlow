import adhesive

# use https://demo.bpmn.io/
from testApplication.ParallelTask import ParallelTask

parallelTask1 = ParallelTask()
parallelTask2 = ParallelTask()
parallelTask3 = ParallelTask()

@adhesive.task("FirstTask")
def firstTask(context):
    pass


@adhesive.task("RepetitiveTask")
def repetitiveTask(context):
    pass


@adhesive.task("ParallelTask1")
def parallelTask1(context):
    print(parallelTask1.execute())


@adhesive.task("ParallelTask2")
def parallelTask2(context):
    print(parallelTask2.execute())


@adhesive.task("ParallelTask3")
def parallelTask3(context):
    print(parallelTask3.execute())


@adhesive.task("CalculateEndTask")
def calculateEndTask(context):
    pass


@adhesive.task("EndFlowTask")
def endFlowTask(context):
    pass


@adhesive.task("Parallelizer")
def parallelizer(context):
    print("Parallelizer")
    for attr in dir(context):
        print("obj.%s = %r" % (attr, getattr(context, attr)))


adhesive.bpmn_build("testApplication/diagram.bpmn", wait_tasks=False)
