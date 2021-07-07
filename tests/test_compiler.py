import pathlib
import unittest
from ..src.classes.pycompiler import PyCompiler
from ..src.classes.domain.pyreader import PyReader

base_dir = pathlib.Path(__file__).parent / pathlib.Path('dummy_src')
test_py_path = base_dir / pathlib.Path('test.py')


class TestCompiler(unittest.TestCase):
    def tearDown(self) -> None:
        test_py_path.with_suffix('.spec').unlink()

    def test_make_spec(self):
        compiler = PyCompiler(test_py_path)
        compiler.make_spec_file()
        self.assertTrue(test_py_path.with_suffix('.spec').exists())


class TestPyReader(unittest.TestCase):
    reader = PyReader(test_py_path)
    package_list = ['pathlib', 'os', 'tkinter']

    def test_load_py_file(self):
        txt_from_reader = self.reader._get_contents()
        with open(test_py_path, 'r') as f:
            txt = f.readlines()

        self.assertEqual(txt_from_reader, txt)

    def test_extract_import(self):
        package_list_from_reader = self.reader.extracct_packages()
        self.assertEqual(self.package_list, package_list_from_reader)


if __name__ == '__main__':
    unittest.main()
