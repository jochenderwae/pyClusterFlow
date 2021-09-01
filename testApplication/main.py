import sys

import adhesive

# use https://demo.bpmn.io/
from testApplication.ParallelTask import ParallelTask

parallelTaskObj1 = ParallelTask()
parallelTaskObj2 = ParallelTask()
parallelTaskObj3 = ParallelTask()


@adhesive.task("FirstTask")
def firstTask(context):
    context.data.count = 3
    context.data.endFlow = False


@adhesive.task("RepetitiveTask")
def repetitiveTask(context):
    pass


@adhesive.task("ParallelTask1")
def parallelTask1(context):
    context.data.parallelTask1Result.append(parallelTaskObj1.execute(context.data.as_dict()))


@adhesive.task("ParallelTask2")
def parallelTask2(context):
    context.data.parallelTask2Result.append(parallelTaskObj2.execute(context.data.as_dict()))


@adhesive.task("ParallelTask3")
def parallelTask3(context):
    context.data.parallelTask3Result.append(parallelTaskObj3.execute(context.data.as_dict()))


@adhesive.task("CalculateEndTask")
def calculateEndTask(context):
    outputs = []
    for attr in dir(context):
        if not attr.startswith("_"):
            outputs.append("context.%s = %r" % (attr, getattr(context, attr)))
    context.data.contextContent = outputs
    context.data.calculateEndTaskResult = "inputs: {}, {}".format(context.data.param1, context.data.param2)
    context.data.count -= 1
    if context.data.count == 0:
        context.data.endFlow = True


@adhesive.task("EndFlowTask")
def endFlowTask(context):
    pass


initial_data = {
    "param1": "One",
    "param2": 2,
    "parallelTask1Result": [],
    "parallelTask2Result": [],
    "parallelTask3Result": [],
}
ret = adhesive.bpmn_build("testApplication/diagram.bpmn", wait_tasks=False, initial_data=initial_data)
if ret:
    ret_dict = ret.as_dict()
    for name in ret_dict:
        if not name.startswith("_"):
            print("{}: {}".format(name, ret_dict[name]))

for item in ret.contextContent:
    print(item)

