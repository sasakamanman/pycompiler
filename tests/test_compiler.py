import pathlib
import unittest
from ..src.classes.pycompiler import PyCompiler
from ..src.classes.domain.pyreader import PyReader
from ..src.classes.domain.package import Package

base_dir = pathlib.Path(__file__).parent / pathlib.Path('dummy_src')
test_py_path = base_dir / pathlib.Path('test.py')
test2_py_path = base_dir / pathlib.Path('test2.py')


class TestCompiler(unittest.TestCase):
    def tearDown(self) -> None:
        test_py_path.with_suffix('.spec').unlink()

    def test_make_spec(self):
        compiler = PyCompiler(test_py_path)
        compiler.make_spec_file()
        self.assertTrue(test_py_path.with_suffix('.spec').exists())


class TestPyReader(unittest.TestCase):
    reader = PyReader(test_py_path)
    reader_recurcive = PyReader(test2_py_path)
    package_list_test = ['pathlib', 'os', 'tkinter']
    package_list_test2 = ['classes', 're']

    def test_load_py_file(self):
        txt_from_reader = self.reader._get_contents()
        with open(test_py_path, 'r') as f:
            txt = f.readlines()

        self.assertEqual(txt_from_reader, txt)

    def test_extract_import(self):
        package_list_from_reader = self.reader.extracct_packages()
        self.assertEqual(self.package_list_test, package_list_from_reader)
    '''
    def test_load_recursively(self):
        package_list_from_reader = self.reader_recurcive.extracct_packages()
        self.assertEqual(self.package_list_test2, package_list_from_reader)
    '''


class TestPackage(unittest.TestCase):
    package_os = 'os'
    test_line_os = f'import {package_os}\n'

    def test_make_package(self):
        package_os = Package(self.test_line_os)
        self.assertEqual(package_os._package, self.package_os)


if __name__ == '__main__':
    unittest.main()
