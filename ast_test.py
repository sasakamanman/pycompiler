import ast

input_item = '''
import os
from src import line_parser

class A:
    import pathlib
    def a(self):
        print('test')

a = A()
a.a()
'''

ast_obj = ast.parse(input_item)
print(ast.dump(ast_obj))
