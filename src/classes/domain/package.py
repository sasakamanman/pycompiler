import re


class Package:
    _import_txt = ' *(from .* )?import '
    _compiler = re.compile(_import_txt)

    def __init__(self, script_line: str) -> None:
        formed_script_line = script_line.replace('\n', '')
        self._package = formed_script_line.split('import ')[-1]
