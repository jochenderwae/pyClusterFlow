import unittest

from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.process_read.bpmn import read_bpmn_file
from test.adhesive.steps.check_equals import assert_equal_steps
from test.adhesive.steps.test_tasks import adhesive, _async


class TestGatewayComplex(unittest.TestCase):
    """
    Test if the process executor can process complex gateways.
    """
    def test_complex_gateway(self):
        """
        Load a process with a gateway and test it..
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/gateway-complex.bpmn")

        process_executor = ProcessExecutor(adhesive.process)
        data = _async(process_executor.execute())

        assert_equal_steps({
            "Test Firefox": 1,
            "Test Chrome": 1,
            "Test Browser chrome on linux": 1,
            "Test Browser firefox on linux": 1,
        }, data.steps)
        self.assertFalse(process_executor.events)

    def test_exclusive_gateway_non_wait(self):
        """
        Load a process with a gateway and test it..
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/gateway-complex.bpmn")

        process_executor = ProcessExecutor(adhesive.process, wait_tasks=False)
        data = _async(process_executor.execute())

        assert_equal_steps({
            "Test Firefox": 1,
            "Test Chrome": 1,
            "Test Browser chrome on linux": 2,
            "Test Browser firefox on linux": 2,
        }, data.steps)
        self.assertFalse(process_executor.events)


if __name__ == '__main__':
    unittest.main()
