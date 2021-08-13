import pathlib
import ast
import sys
from typing import List, Set, Union

_init_path = pathlib.Path('__init__.py')


def parse_file(target_path: pathlib.Path, package_set: Set[str] = set()) -> Set[str]:
    target_file = _get_target_file(target_path)
    base_dir = target_file.parent
    ast_file = _make_ast(target_file)
    for node in ast.iter_child_nodes(ast_file):
        _parse_node(node, base_dir, package_set)
    return package_set


def _make_ast(target_file: pathlib.Path) -> ast.AST:
    with open(target_file) as f:
        ast_file = ast.parse(f.read())
    return ast_file


def _parse_node(node: ast.AST, base_dir: pathlib.Path,
                package_set: Set[str]) -> Set[str]:
    if isinstance(node, ast.Import):
        _parse_import(node, base_dir, package_set)
    if isinstance(node, ast.ImportFrom):
        _parse_import_from(node, base_dir, package_set)
    for sub_node in ast.iter_child_nodes(node):
        _parse_node(sub_node, base_dir, package_set)
    return package_set


def _get_target_file(target_path: pathlib.Path) -> pathlib.Path:
    if target_path.suffix == '.py': return target_path
    if not target_path.is_dir():
        raise SystemError(f'{str(target_path)} is not a python file')

    target_file = target_path / _init_path
    if not target_file.exists():
        raise FileExistsError(f'{str(target_file)} is not found')
    return target_file


def _parse_import(node: ast.Import, base_dir: pathlib.Path,
                  package_set: Set[str]) -> Set[str]:
    for item in node.names:
        splited_name = item.name.split('.')
        package_set = _parse_imported_name(splited_name, base_dir, package_set)
    return package_set


def _parse_imported_name(splited_name: List[str], base_dir: pathlib.Path,
                         package_set: Set[str]) -> Set[str]:
    item_path_abs = _find_path_abs(splited_name[0], base_dir)
    if not item_path_abs: return package_set

    for idx, name in enumerate(splited_name):
        if idx == 0: continue

        module_path_abs = _find_path_abs_from_base(name, item_path_abs.parent)
        if module_path_abs is None: break
        item_path_abs = module_path_abs

    package_set = parse_file(item_path_abs, package_set)

    return package_set


def _parse_import_from(node: ast.ImportFrom, base_dir: pathlib.Path,
                       package_set: Set[str]) -> Set[str]:
    if not isinstance(node.module, str): return package_set
    module_path_abs = _find_path_abs(node.module, base_dir)

    if not module_path_abs: return package_set

    module_dir_path_abs = module_path_abs.parent

    for item in node.names:
        item_path_abs = _find_path_abs_from_base(item.name, module_dir_path_abs)
        if not item_path_abs: continue
        package_set = parse_file(item_path_abs, package_set)
    return package_set


def _find_path_abs(name: str, base_dir: pathlib.Path) -> Union[pathlib.Path, None]:
    path_in_base_dir = _find_path_abs_from_base(name, base_dir)
    if path_in_base_dir: return path_in_base_dir

    for path in sys.path:
        path_in_sys_path = path / pathlib.Path(f'{name}.py')
        if path_in_sys_path.exists(): return path_in_sys_path

        path_in_sys_path_with_init = path / pathlib.Path(name) / _init_path
        if path_in_sys_path_with_init.exists(): return path_in_sys_path_with_init

        path_in_sys_path_as_dir = path / pathlib.Path(name)
        if path_in_sys_path_as_dir.exists(): return path_in_sys_path_as_dir

    return None


def _find_path_abs_from_base(name: str, base_dir: pathlib.Path) -> Union[pathlib.Path, None]:
    path_in_base_dir = base_dir / pathlib.Path(f'{name}.py')
    if path_in_base_dir.exists(): return path_in_base_dir

    path_in_sys_path_with_init = base_dir / pathlib.Path(name) / _init_path
    if path_in_sys_path_with_init.exists(): return path_in_sys_path_with_init

    path_in_sys_path_as_dir = base_dir / pathlib.Path(name)
    if path_in_sys_path_as_dir.exists(): return path_in_sys_path_as_dir
    return None
