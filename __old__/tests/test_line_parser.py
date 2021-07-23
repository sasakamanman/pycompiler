from typing import Callable, List
import unittest
import pathlib
from unittest import mock
from ..src.line_parser import parse_package, parse_imported_file, ParseRejectError

package_name_os = 'os'
package_name_tk = 'tkinter'
module_name_ttk = 'ttk'
text_import = 'import '
text_from = 'from '
space = '    '
import_text_os = text_import + package_name_os
import_text_ttk = text_from + package_name_tk + text_import + module_name_ttk


class TestPackageParser(unittest.TestCase):
    def test_get_top_package(self):
        imported_package = parse_package(import_text_os)
        self.assertEqual(imported_package, package_name_os)

    def test_get_package_from_module_import(self):
        imported_package = parse_package(import_text_ttk)
        self.assertEqual(imported_package, package_name_tk)

    def test_get_package_with_as(self):
        imported_package = parse_package(import_text_os + ' as test')
        self.assertEqual(imported_package, package_name_os)

    def test_package_extraction(self):
        text_import = 'from tkinter.ttk import Treeview'
        imported_package = parse_package(text_import)
        self.assertEqual(imported_package, package_name_tk)

    def test_imported_item_is_not_package(self):
        text_import = 'from testmod import tester'
        imported_package = parse_package(text_import)
        self.assertIsNone(imported_package)

    def test_raise_exception_with_multi_import(self):
        text_import = import_text_os + ', ' + package_name_tk
        with self.assertRaises(ParseRejectError):
            parse_package(text_import)


import_name_foo = 'foo'
import_name_bar = 'bar'
import_name_baz = 'baz'
import_text_foo = text_import + import_name_foo
base_dir = 'C:/abc'
import_foo_file_path = base_dir + '/' + import_name_foo
import_bar_file_path = base_dir + '/' + import_name_bar
import_foo_bar_file_path = '/'.join([base_dir, import_name_foo, import_name_bar])

text_import_foo_bar = text_from + import_name_foo + text_import + import_name_bar


mocked_os_stat = mock.MagicMock()


def side_effect_os_stat(value: pathlib.Path) -> None:
    if not str(value)[-3:] == '.py': raise ValueError


def make_side_effect_os_args_is_not_file(target_list: List[str]) -> Callable:
    def side_effect_os_stat(value: pathlib.Path) -> None:
        for target in target_list:
            if target in str(value): raise ValueError
    return side_effect_os_stat


@mock.patch('pathlib._NormalAccessor.stat', new=mocked_os_stat)
@unittest.skip('refactoring')
class TestImportedFileParserOld(unittest.TestCase):
    def setUp(self) -> None:
        mocked_os_stat.reset_mock(side_effect=True)

    def test_get_imported_file_path(self):
        imported_file = parse_imported_file(import_text_foo, base_dir)
        self.assertEqual(imported_file, import_foo_file_path)
        import_text_as = import_text_foo + ' as baz'
        imported_file = parse_imported_file(import_text_as, base_dir)
        self.assertEqual(imported_file, import_foo_file_path)

    def test_imported_non_exist_file(self):
        mocked_os_stat.side_effect = ValueError
        imported_file = parse_imported_file(import_text_foo, base_dir)
        self.assertIsNone(imported_file)

    def test_imported_file_is_py_sile(self):
        import_py_file_path = import_foo_file_path + '.py'
        mocked_os_stat.side_effect = side_effect_os_stat
        imported_file = parse_imported_file(import_text_foo, base_dir)
        self.assertEqual(imported_file, import_py_file_path)

    def test_raise_exception_with_multi_import(self):
        text_import = import_text_foo + ', baz'
        with self.assertRaises(ParseRejectError):
            parse_imported_file(text_import, base_dir)

    def test_get_from_file_from_import_line(self):
        mocked_os_stat.side_effect = make_side_effect_os_args_is_not_file(['foo/bar.py', 'foo/bar'])
        imported_file = parse_imported_file(text_import_foo_bar, base_dir)
        self.assertEqual(imported_file, import_foo_file_path)

    @unittest.skip('it\'s dificult test')
    def test_get_import_file_from_import_line(self):
        mocked_os_stat.side_effect = make_side_effect_os_args_is_not_file([import_name_foo])
        imported_file = parse_imported_file(text_import_foo_bar, base_dir)
        self.assertEqual(imported_file, import_foo_bar_file_path)

    @unittest.skip('it\'s dificult test')
    def test_get_import_preferentially_foo(self):
        imported_file = parse_imported_file(text_import_foo_bar, base_dir)
        self.assertEqual(imported_file, import_foo_file_path)
