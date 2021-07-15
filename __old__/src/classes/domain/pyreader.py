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
        '''
        for package in package_list:
            package_path = self._py_path.parent / pathlib.Path(package)
            if not package_path.exists(): continue
            sub_reader = PyReader(package_path)
            package_list_from_sub = sub_reader.extracct_packages()
            package_list += package_list_from_sub
        '''
        return package_list


if __name__ == '__main__':
    pass
