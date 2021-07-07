import pathlib
import re
from typing import List


class PyReader:
    _import_txt = 'import '
    _compiler = re.compile(_import_txt)

    def __init__(self, py_path: pathlib.Path) -> None:
        self._py_path = py_path

    def _get_contents(self) -> List[str]:
        with open(self._py_path, 'r') as f:
            txt = f.readlines()

        return txt

    def extracct_packages(self) -> List[str]:
        txt = self._get_contents()
        package_list: List[str] = []
        for line in txt:
            if not self._compiler.search(line): continue
            splited_line = line.split(' ')[1].replace('\n', '')
            package_list.append(splited_line)

        return package_list


if __name__ == '__main__':
    pass
