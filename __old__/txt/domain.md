### PackageParser
* [X] ~~*parse script line*~~ [2021-07-19]
* [X] ~~*get `foo` on recieving `import foo`*~~ [2021-07-19]
* [X] ~~*get `foo` on recieving `import foo as baz`*~~ [2021-07-19]
* [X] ~~*get `foo` on recieving `from foo import bar`*~~ [2021-07-19]
* [X] ~~*get `foo` on recieving `from foo.bar import baz`*~~ [2021-07-19]
* [X] ~~*if imported py file or dir exists in pythonpath, return package name*~~ [2021-07-20]
* [X] ~~*if imported py file or dir doesn't exist in pythonpath, return None*~~ [2021-07-20]
* [X] ~~*doesn't deal with multi import. therefore before parse, divide these packages to several lines.*~~ [2021-07-22]

### ImportedFileParser
* [ ] get `foo` path on recieving `import foo`
* [ ] get `foo` path on recieving `import foo as baz`
* [ ] get `foo` path on recieving `from foo import bar` when `foo/bar` is not file or dir
* [ ] get `bar` path on recieving `from foo import bar` when `foo/bar` is a file or dir and `foo` isn't a py file
* [ ] get `foo` path on recieving `from foo import bar` when `bar` and `foo` are files
* [ ] get `bar` path on recieving `from foo.bar import baz` when `baz` is not file or dir
* [ ] get `baz` path on recieving `from foo.bar import baz` when `baz` is file or dir
* [ ] get `baz` path on recieving `from foo.bar import baz as qux` when `baz` is file or dir
* [ ] get `qux` path on recieving `from foo.bar import baz.qux` when `qux` is file or dir
* [ ] get `baz` path on recieving `from foo.bar import baz.qux` when `qux` isn't file or dir and `baz` is file or dir
* [ ] return file or dir abs path
* [ ] if imported file or dir doesn't exist in base path, return None
* [ ] does it works when imported item is py file?
* [ ] doesn't deal with multi import. therefore before parse, divide these packages to several lines.
* [ ] doesn't deal with multi import. therefore before parse, divide these packages to several lines.
* [ ] when bar.py and baz.py exists and line `from foo.bar import baz` is passed, does function return bar.py?
* [X] ~~*check priority of import when `from foo import bar` is passed and foo.py and foo/bar.py exist*~~ [2021-07-22]
  * when foo.py and foo/bar.py exist, foo.py is imported preferentially
  *  python raises ImportError if bar is not in foo.py

### LineParser
#### First Step: Only get imported item and tree shake isn't executed
* [ ] divide line by ',' and ';' properly
* [ ] return `None` if line not includes `import`
* [ ] return set of package and py file if line includes `import`
* [ ] recurcively make FileParser and get packages and py file imported

### FileParser
#### First Step: Only get imported item and tree shake isn't executed
* [ ] recieve py file
* [ ] return package list
* [ ] split code by semi-colon
* [ ] read file recursiely