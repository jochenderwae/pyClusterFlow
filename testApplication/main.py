import adhesive

# use https://demo.bpmn.io/

@adhesive.task("FirstTask")
def firstTask(context):
    pass


@adhesive.task("RepetitiveTask")
def repetitiveTask(context):
    pass


@adhesive.task("ParallelTask1")
def parallelTask1(context):
    pass


@adhesive.task("ParallelTask2")
def parallelTask2(context):
    pass


@adhesive.task("ParallelTask3")
def parallelTask3(context):
    pass


@adhesive.task("CalculateEndTask")
def calculateEndTask(context):
    context.data.navigation_direction = "forward"
    pass


@adhesive.task("EndFlowTask")
def endFlowTask(context):
    pass


@adhesive.task("Parallelizer")
def parallelizer(context):
    print("Parallelizer")
    for attr in dir(context):
        print("obj.%s = %r" % (attr, getattr(context, attr)))


adhesive.bpmn_build("testApplication/MainProcess.bpmn")
