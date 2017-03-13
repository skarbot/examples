import builtins
from unittest.mock import patch
from unittest import TestCase, main


def module_check():
    try:
        import abc
    except ImportError:
        return 1

realimport = builtins.__import__
def myimport(name, globals, locals, fromlist, level):
    if name == 'abc':
        raise ImportError
    return realimport(name, globals, locals, fromlist, level)


class TestModuleImport(TestCase):
    def test(self):
        with patch('builtins.__import__', myimport):
            self.assertEqual(module_check(), 1)
    def test1(self):
        with patch('builtins.__import__', myimport):
            with self.assertRaises(ImportError):
                import abc

if __name__ == '__main__':
    main()
