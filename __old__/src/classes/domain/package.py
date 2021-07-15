import re
from typing import Union


class ImportedModule:
    _import_txt = ' *(from .* )?import '
    _compiler = re.compile(_import_txt)

    def __init__(self, imported_item: str, parent: Union[str, None] = None) -> None:
        self._imported_item = imported_item.replace(' ', '')
        self._parent = parent.replace(' ', '') if isinstance(parent, str) else parent

    def get_package(self) -> str:
        return self._imported_item if not self._parent else self._parent

    @property
    def is_package(self) -> bool:
        return True

    @staticmethod
    def parseLine(line: str) -> Union['ImportedModule', None]:
        formated_line = line.replace('\n', '')
        if not ImportedModule._compiler.match(formated_line):
            return None
        if 'from ' in formated_line:
            return ImportedModule._extract_import_and_from(formated_line)
        return ImportedModule._extract_only_import(formated_line)

    @staticmethod
    def _extract_import_and_from(line: str) -> 'ImportedModule':
        splited_str = re.split('from | import ', line)
        return ImportedModule(splited_str[-1], splited_str[-2])

    @staticmethod
    def _extract_only_import(line: str) -> 'ImportedModule':
        line_as_removed = line.split(' as ')[0]
        imported_item = line_as_removed.split('import ')[-1]
        return ImportedModule(imported_item)
