from unittest import TestCase, main
from unittest.mock import patch

from . import production


class MockProductionClass():
    def __init__(self, param):
        print('my production class')
        self.param = param

    def run(self):
        print(self.param)
        return self.param

class TestPatch(TestCase):
    @patch('production.ProductionClass')
    def test1(self, MockProductionClass):
        assert production.ProductionClass is MockProductionClass

    def test2(self):
        with patch('production.ProductionClass', MockProductionClass):
            assert production.ProductionClass is MockProductionClass

if __name__ == '__main__':
    main()