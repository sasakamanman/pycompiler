## file parser (using ast)
* [X] ~~*which is it domain or function?*~~ [2021-07-26]
* [X] ~~*recieve path*~~ [2021-07-26]
* [X] ~~*return imported package str set (not file set)*~~ [2021-07-28]
* [X] ~~*when recieved path is file, load file*~~ [2021-07-28]
* [X] ~~*when recieved path is dir, search __init__.py and load __init__.py*~~ [2021-07-28]
* [X] ~~*if recieved path is dir and __init__.py doesn't exist, throw Exception*~~ [2021-07-28]
* [X] ~~*if recieved path is nether dir nor py file, throw Exception*~~ [2021-07-28]
* [X] ~~*when no package or module is imported, return void set*~~ [2021-07-28]
* [X] ~~*how to search Import or ImportFrom from AST? access member iterately?*~~ [2021-07-29]
* [ ] when _parse_node recieve `Import` or `ImportFrom`, get imported package
* [X] ~~*ehwn _parse_node recieve `Import` or `ImportFrom`, run import parser*~~ [2021-07-29]
* [X] ~~*split by `.` to search path*~~ [2021-08-06]
* [X] ~~*for each names splited by `.`, run `_find_path_abs` with first name and `_find_path_abs_from_base` with the others names by `_parse_import`*~~ [2021-08-06]
* [ ] if first name isn't found, return instantly
  * when first name isn't found?
    * [X] ~~*imported package or module is included in python interprinter*~~ [2021-08-06]
    * [ ] such file doesn't exist
  * is second term unnecessaly because interprinter raises `ModuleNotFoundError` on testing code before complie?
* [ ] if first name isn't found, add name to `package_set`
* [ ] add package name to `package_set` when path is normal py file and parent path is pythonpath 
* [ ] add package name to `package_set` path is `__init__.py` and grandparent path is in pythonpath
* [ ] if second or afterward name isn't found and beforehand path is py file, return instantly
* [ ] for each names splited by `.`, run `_find_path_abs` with first name and `_find_path_abs_from_base` with the others names by `_parse_import_from`
* [ ] on file search, get top pathes and digging these
* [X] ~~*when imported item is py file and found in pythonpath by `_parse_import`, run `parse_file`*~~ [2021-08-03]
* [X] ~~*when imported item is py file and found in pythonpath by `_parse_import_from`, run `parse_file`*~~ [2021-08-05]
* [ ] when imported item is found in pythonpath by `_parse_import` and import line doesn't include `.`, add item name to `package_set`
* [ ] when imported package is found in pythonpath by `_parse_import_from` and `from` block doesn't include `.`, add package name to `package_set`
* [ ] when imported package is found in pythonpath by `_parse_import` and `import` block includes `.`, add top name to `package_set` and try to find sub name path by `_find_path_abs_from_base`
* [ ] when imported package is found in pythonpath by `_parse_import_from` and `import` block includes `.`, add top name to `package_set` and try to find sub name path by `_find_path_abs_from_base`
* [X] ~~*when `_find_path_abs_from_base` returns None, its a C file or built-in. therefor return package set instantly.*~~ [2021-08-03]
* [X] ~~*when `_find_path_abs` returns None, its a C file or built-in. therefor return package set instantly.*~~ [2021-08-04]
* [X] ~~*to search py file in work directory, `_parse_import` recieve base_dir*~~ [2021-07-29]
* [X] ~~*to search py file in work directory, `_parse_import_from` recieve base_dir*~~ [2021-07-29]