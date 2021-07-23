### import patern
- import member from file directry
- import member from file relatively
- import file directry
- import file relatively
- import member from module
- import member from package
- import module from package
- import module or package
- using 'as foo'

### first step: only include neccesaly file and package
#### import member from file directry
#### import member from file relatively
#### import file directry
#### import file relatively
- get file with same directory tree
- if need, make \_\_init\_\_.py for every directory
- **at first step, ignore these patterns**

#### import member from module
#### import member from package
#### import module from package
- add parent to package list
- **at first step, ignore default modules**

#### import module
#### import package
- add imported item to package list

### using 'as foo'
- delete as and name

### other import behaviors
- when dir `foo` is importted, only members in __init__.py is callable
- when foo.py and foo/bar.py exist, script `from foo import bar` attempts importing bar from foo.py regardless of which foo.py has bar member