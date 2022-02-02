import os
import unittest

from oopnet.elements import Network
from oopnet.writer import Write
from oopnet.reader import Read
from base import CTownModel, MicropolisModel, PoulakisEnhancedPDAModel, RulesModel, SimpleModel


def write_read(network: Network) -> Network:
    filename = os.path.join('tmp', 'test.inp')
    Write(network, filename)
    new_network = Read(filename)
    os.remove(filename)
    return new_network


class CTownWriterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = CTownModel()

    def test_write_read(self):
        new_network = write_read(self.model.network)
        self.assertEqual(self.model.network, new_network)


class MicropolisWriterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = MicropolisModel()

    def test_write_read(self):
        new_network = write_read(self.model.network)
        self.assertEqual(self.model.network, new_network)


class PoulakisEnhancedPDAWriterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = PoulakisEnhancedPDAModel()

    def test_write_read(self):
        new_network = write_read(self.model.network)
        self.assertEqual(self.model.network, new_network)


class RulesModelWriterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = RulesModel()

    def test_write_read(self):
        new_network = write_read(self.model.network)
        self.assertEqual(self.model.network, new_network)


class SimpleModelWriterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SimpleModel()

    def test_write_read(self):
        new_network = write_read(self.model.network)
        self.assertEqual(self.model.network, new_network)


if __name__ == '__main__':
    unittest.main()
