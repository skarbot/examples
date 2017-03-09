from unittest.mock import patch, Mock

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


def with_spec():
    mock = Mock()
    mock.one()

    mock = Mock(spec=['test', 'test1'])
    # Raises attribute error
    try:
        mock.one()
    except AttributeError:
        pass

    mock = Mock(spec=MockProductionClass)
    mock.run()
    # Attribute error
    mock.process()


def side_effects():
    def one():
        return 5
    mock = Mock(one=one)
    mock.one = Mock()
    mock.one.side_effect = [5,6,7]
    print(mock.one())
    print(mock.one())
    print(mock.one())

@patch.multiple('production', ProductionClass=MockProductionClass, ProductionClass2=MockProductionClass)
def patch_multiple():
    p1 = production.ProductionClass(5)
    print(p1.run())


@patch.object(production.ProductionClass, 'process', return_value=5)
def patch_object(mock):
    print(mock)
    p = production.ProductionClass(param='test')
    print(p.process())


'''
with patch('production.ProductionClass') as MockClass:
    p = MockClass()
    m = MockClass.return_value
    print(m.method)
    m.method.return_value='test'
    print(m.method())
    print(p.method())
'''


patch_object()