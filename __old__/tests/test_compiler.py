import pathlib
import unittest
import sys
from ..src.classes.pycompiler import PyCompiler
from ..src.classes.domain.pyreader import PyReader
from ..src.classes.domain.package import ImportedModule

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


class TestImportedModule(unittest.TestCase):
    package_os = 'os'
    test_line_os = f'import {package_os}\n'
    package_tk = 'tkinter'
    module_ttk = 'ttk'
    test_line_ttk = f'from {package_tk} import {module_ttk}'
    python_path = sys.path[-1]

    def test_make_package(self):
        package_os = ImportedModule.parseLine(self.test_line_os)
        self.assertEqual(package_os._imported_item, self.package_os)
        self.assertEqual(package_os._imported_item_path, self.python_path + '\\' + self.package_os)
        package_none = ImportedModule.parseLine('aaaaa')
        self.assertFalse(package_none)

    def test_get_package_and_module(self):
        package_tk = ImportedModule.parseLine(self.test_line_ttk)
        self.assertEqual(package_tk._parent, self.package_tk)
        self.assertEqual(package_tk._imported_item, self.module_ttk)

    def test_remove_space(self):
        test_line = f'from {self.package_tk}   import {self.module_ttk}    '
        package_tk = ImportedModule.parseLine(test_line)
        self.assertEqual(package_tk._parent, self.package_tk)
        self.assertEqual(package_tk._imported_item, self.module_ttk)

    def test_return_module(self):
        package_os = ImportedModule.parseLine(self.test_line_os)
        self.assertEqual(package_os.get_package(), self.package_os)
        package_tk = ImportedModule.parseLine(self.test_line_ttk)
        self.assertEqual(package_tk.get_package(), self.package_tk)

    def test_del_as_foo(self):
        test_line_os = self.test_line_os + ' as oooo'
        package_os = ImportedModule.parseLine(test_line_os)
        self.assertEqual(package_os.get_package(), self.package_os)
        test_line_tk = self.test_line_ttk + ' as tkkkkkk'
        package_tk = ImportedModule.parseLine(test_line_tk)
        self.assertEqual(package_tk.get_package(), self.package_tk)

    @unittest.skip('test to get dir before it')
    def test_check_is_package(self):
        test_line_sub_file = 'from .src import test'
        imported_file = ImportedModule.parseLine(test_line_sub_file)
        self.assertFalse(imported_file.is_package)
        package_os = ImportedModule.parseLine(self.test_line_os)
        self.assertTrue(package_os.is_package)


if __name__ == '__main__':
    unittest.main()
