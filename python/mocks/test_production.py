from unittest import TestCase, main
from unittest.mock import patch

from mocks import production


class MockProductionClass():
    def __init__(self, param):
        print('my production class')
        self.param = param

    def run(self):
        print(self.param)
        return self.param

class TestPatch(TestCase):
    @patch('mocks.production.ProductionClass', MockProductionClass)
    def test1(self):
        assert production.ProductionClass is MockProductionClass

    def test2(self):
        with patch('mocks.production.ProductionClass', MockProductionClass):
            assert production.ProductionClass is MockProductionClass

class TestPatcher(TestCase):
    def setUp(self):
        self.patch1 = patch('mocks.production.ProductionClass', MockProductionClass)
        self.patch1.start()

    def tearDown(self):
        self.patch1.stop()

    def test(self):
        assert production.ProductionClass is MockProductionClass


if __name__ == '__main__':
    main()