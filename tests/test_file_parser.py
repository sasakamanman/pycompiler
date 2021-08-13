import pathlib
import unittest
import ast
import sys
from typing import List, Set
from unittest import mock
from src.functions.parse_file import parse_file, _parse_import, _parse_import_from


class MockedImport(mock.MagicMock):
    def __init__(self, names: List[str]) -> None:
        super().__init__()
        self.names = [ast.alias(name) for name in names]


class MockedImportFrom(mock.MagicMock):
    def __init__(self, module: str, names: List[str]) -> None:
        super().__init__()
        self.names = [ast.alias(name) for name in names]
        self.module = module


def mocked_parse_file_function(target_path: pathlib.Path, package_set: Set[str] = set()):
    return package_set


class TestFileParser(unittest.TestCase):
    base_dir = pathlib.Path(__file__).parent / pathlib.Path('targets')
    sub_dir = base_dir / pathlib.Path('sub')

    file_foo_relative = pathlib.Path('foo.py')
    file_foo_abs = base_dir / file_foo_relative

    file_bar_relative = pathlib.Path('bar.py')
    file_bar_abs = base_dir / file_bar_relative

    def setUp(self):
        sys.setrecursionlimit(200)

    def test_parser_interface(self):
        package_list = parse_file(self.file_foo_abs)
        self.assertEqual(package_list, set())

    def test_parser_get_init_py(self):
        package_list = parse_file(self.sub_dir)
        self.assertEqual(package_list, set())

    @mock.patch('src.functions.parse_file._parse_import')
    @mock.patch('src.functions.parse_file._parse_import_from')
    def test_run_import_parser(self, mocked_parse_import: mock.MagicMock,
                               mocked_parse_import_from: mock.MagicMock):
        parse_file(self.file_bar_abs)
        self.assertTrue(mocked_parse_import.called)
        self.assertTrue(mocked_parse_import_from.called)

    @mock.patch('src.functions.parse_file.parse_file')
    def test_parse_import_call_parse_file(self, mocked_parse_file: mock.MagicMock):
        mocked_import = MockedImport(['tkinter'])
        _parse_import(mocked_import, self.base_dir, set())
        self.assertTrue(mocked_parse_file.called)

    @unittest.skip('circurated import is occured')
    def test_parse_import_from(self):
        mocked_import_from = MockedImportFrom('tkinter', ['ttk'])
        _parse_import_from(mocked_import_from, self.base_dir, set())

    @mock.patch('src.functions.parse_file.parse_file')
    def test_parse_import_from_call_parse_file(self, mocked_parse_file: mock.MagicMock):
        mocked_import_from = MockedImportFrom('tkinter', ['ttk'])
        _parse_import_from(mocked_import_from, self.base_dir, set())
        self.assertTrue(mocked_parse_file.called)

    @mock.patch('src.functions.parse_file.parse_file', side_effect=mocked_parse_file_function)
    def test_parse_import_split_by_period(self, mocked_parse_file: mock.MagicMock):
        mocked_import = MockedImport(['tkinter.ttk'])
        package_set = _parse_import(mocked_import, self.base_dir, set())
        self.assertTrue(mocked_parse_file.call_count == 1)
        self.assertEqual(mocked_parse_file.call_args[0][0].stem, 'ttk')
        self.assertEqual(package_set, set(['tkinter']))

    def test_parser_raise_invalid_file(self):
        with self.assertRaises(SystemError):
            parse_file(self.file_foo_abs.with_suffix('.html'))
        with self.assertRaises(FileExistsError):
            parse_file(self.base_dir)


if __name__ == '__main__':
    unittest.main()
