import pathlib


class PyCompiler:
    def __init__(self, py_path: pathlib.Path) -> None:
        self._py_path = py_path

    def make_spec_file(self) -> None:
        self._spec_path = self._py_path.with_suffix('.spec')
        with open(self._spec_path, 'a') as f:
            print('test', file=f)
