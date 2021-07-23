import re
import sys
import pathlib
from typing import Union

compiler_text_from_import = re.compile(r' *import | *from | *as ')


class ParseRejectError(Exception):
    def __init__(self, line: str) -> None:
        super().__init__(f'line "{line}" is rejected because it includes "," or ";".')


def parse_package(line: str) -> Union[str, None]:
    _check_parsable_line(line)
    splitted_text = compiler_text_from_import.split(line)
    package = splitted_text[1].split('.')[0]
    return package if _check_is_package(package) else None


def _check_parsable_line(line: str) -> None:
    if ',' in line or ';' in line:
        raise ParseRejectError(line)


def _check_is_package(package: str) -> bool:
    pythonpath_list = [pathlib.Path(path) for path in sys.path]
    package_py_relative_path = pathlib.Path(package + '.py')
    package_dir_relative_path = pathlib.Path(package)
    for idx, base_path in enumerate(pythonpath_list):
        if idx == 0: continue

        package_py_abs_path = base_path / package_py_relative_path
        if package_py_abs_path.exists(): return True

        package_dir_abs_path = base_path / package_dir_relative_path
        if package_dir_abs_path.exists(): return True

    return False


def parse_imported_file(line: str, base_dir: str) -> Union[str, None]:
    _check_parsable_line(line)
    splitted_text = compiler_text_from_import.split(line)[:-1]

    for imported_file in splitted_text[1:]:
        imported_file_abs_path = pathlib.Path(base_dir) / pathlib.Path(imported_file)
        if imported_file_abs_path.exists(): return str(imported_file_abs_path)

        imported_file_abs_path = imported_file_abs_path.with_suffix('.py')
        if imported_file_abs_path.exists(): return str(imported_file_abs_path)
    return None
