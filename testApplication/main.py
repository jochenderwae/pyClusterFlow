import sys

import adhesive

# use https://demo.bpmn.io/
from adhesive import AdhesiveProcess
from testApplication.ParallelTask import ParallelTask, RepetitiveTask


@adhesive.task("FirstTask")
def firstTask(context):
    context.data.count = 3
    context.data.endFlow = False


RepetitiveTask.bindToDefinition("RepetitiveTask")
ParallelTask.bindToDefinition("ParallelTask1")
ParallelTask.bindToDefinition("ParallelTask2")
ParallelTask.bindToDefinition("ParallelTask3")


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


print(adhesive.process.task_definitions)


initial_data = {
    "param1": "One",
    "param2": 2,
    "ParallelTask_data": []
}
ret = adhesive.bpmn_build("testApplication/diagram.bpmn", wait_tasks=False, initial_data=initial_data)
if ret:
    ret_dict = ret.as_dict()
    for name in ret_dict:
        if not name.startswith("_"):
            print("{}: {}".format(name, ret_dict[name]))

for item in ret.contextContent:
    print(item)
