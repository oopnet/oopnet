import unittest

from oopnet.report import *
from testing.base import CTownModel, MicropolisModel, PoulakisEnhancedPDAModel, RulesModel, SimpleModel, \
    activate_all_report_parameters


class CTownSimulatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = CTownModel()
        activate_all_report_parameters(self.model.network)
        self.rpt = self.model.network.run()

    def test_pressure(self):
        # p = Pressure()
        # rpt = Run(self.model.network)
        p = self.rpt.pressure
        print(self.rpt)


class MicropolisSimulatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = MicropolisModel()

    # def test_write_read(self):
    #     new_network = write_read(self.model.network)
    #     self.assertEqual(self.model.network, new_network)


class PoulakisEnhancedPDASimulatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = PoulakisEnhancedPDAModel()

    # def test_write_read(self):
    #     new_network = write_read(self.model.network)
    #     self.assertEqual(self.model.network, new_network)


class RulesModelSimulatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = RulesModel()

    # def test_write_read(self):
    #     new_network = write_read(self.model.network)
    #     self.assertEqual(self.model.network, new_network)


class SimpleModelSimulatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SimpleModel()

    # def test_write_read(self):
    #     new_network = write_read(self.model.network)
    #     self.assertEqual(self.model.network, new_network)


if __name__ == '__main__':
    unittest.main()
