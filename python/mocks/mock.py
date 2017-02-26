from unittest.mock import patch

import production


class MockProductionClass():
    def __init__(self, param):
        print('my production class')
        self.param = param

    def run(self):
        print(self.param)
        return self.param

def test(*args, **kwargs):
    return MockProductionClass


@patch('production.ProductionClass', new_callable=test)
def example_with_callable(my_mock_class):
    result = production.ProductionClass == my_mock_class
    t = production.ProductionClass('test')
    print(t.param)
    print(t.run())
    print(result)

@patch('production.ProductionClass', MockProductionClass)
def example_with_callable(my_mock_class):
    result = production.ProductionClass == my_mock_class
    t = production.ProductionClass('test')
    print(t.param)
    print(t.run())
    print(result)


def with_context_manager():
    with patch('production.ProductionClass', MockProductionClass):
        t = production.ProductionClass('test')
        print(t.run())
        result = production.ProductionClass == MockProductionClass
        print(result)
'''
test1()