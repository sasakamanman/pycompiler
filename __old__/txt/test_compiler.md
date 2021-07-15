### Compiler
- run "pyinstaller test.py"
- run "pyinstaller test.spec"
- ~~make spec file~~
- extract imported packages
- extract from packages

### PyReader
- ~~load python file~~
- ~~extract imported package~~
- ~~extract from packages~~
- load python file recurcively if file located in sub directory
- how deal with relative import?

### ImportedModule
- ~~get package~~
- get package from all import pattern
- ~~get package from module pattern~~
- get dir
- ~~factory method~~
- ~~factory returns None if package isn't imported~~
- get package path
- get some import in a line
- get package if imported item is a member or module
- ~~delete space from imported_item and parent~~
- how to check imported item is a package?
- ~~if imported item has changed name by 'as', delete 'as foo'~~

### import patern
- import member from file directry
- import member from file relatively
- import file directry
- import file relatively
- import member from module
- import member from package
- ~~import module from package~~
- ~~import module~~

### first step: only exclude unneccesaly file and package
#### import member from file directry
#### import member from file relatively
#### import file directry
#### import file relatively
- get file with same directory tree
- if need, make \_\_init\_\_.py for every directory
- at first step, ignore these patterns

#### import member from module
#### import member from package
#### import module from package
- add parent to package list

#### import module
#### import package
- add imported item to package list