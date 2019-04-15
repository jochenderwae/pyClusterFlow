from typing import cast
import unittest

from adhesive.graph.SubProcess import SubProcess
from adhesive.xml.bpmn import read_bpmn_file


class TestReadingBpmn(unittest.TestCase):
    """
    Test if we can read a BPMN file correctly.
    """

    def test_reading_bpmn(self) -> None:
        """
        Try to see if reading a basic BPMN works.
        """
        workflow = read_bpmn_file("test/adhesive/xml/adhesive.bpmn")

        self.assertEqual(6, len(workflow.tasks))
        self.assertEqual(6, len(workflow.edges))
        self.assertEqual(1, len(workflow.start_events))
        self.assertEqual(1, len(workflow.end_events))

        first_task = workflow.tasks["_3"]
        self.assertEqual("Build Germanium Image", first_task.name)

        self.assertTrue(workflow)

    def test_reading_subprocess_bpmn(self) -> None:
        workflow = read_bpmn_file("test/adhesive/xml/adhesive_subprocess.bpmn")

        self.assertEqual(5, len(workflow.tasks))
        self.assertEqual(4, len(workflow.edges))
        self.assertEqual(1, len(workflow.start_events))
        self.assertEqual(1, len(workflow.end_events))

        subprocess = cast(SubProcess, workflow.tasks["_7"])
        self.assertEqual("Test Browsers", subprocess.name)

        self.assertEqual(3, len(subprocess.tasks))
        self.assertEqual(1, len(subprocess.edges))
        self.assertEqual(2, len(subprocess.start_events))
        self.assertEqual(0, len(subprocess.end_events))


if __name__ == '__main__':
    unittest.main()
