from RestrictedPython import compile_restricted as compile

from RestrictedPython import safe_builtins
from RestrictedPython import limited_builtins
from RestrictedPython import utility_builtins

import sys

code = """
thing = "HI"

#print(globals().keys(), locals().keys())

def method(a):
    print(a)

class Thing:
    def __init__(self):
        print(super)
        self.hi = "hi"
        method(self.hi)
        method(thing)

thing = Thing()
"""

"""
class Hello:
    def __init__(self):
        print(globals()['__builtins__'].__dict__.keys())
        print(locals()['__class__'].__dict__['__init__'].__dict__)
        print(locals()['self'].keys())
        print(super)


hello = Hello()
print(1/0)
"""

def write_call(obj):
    if isinstance(obj, type(sys)):
        raise RuntimeError('Can\'t write to modules.')

    elif isinstance(obj, type(lambda: 1)):
        raise RuntimeError('Can\'t write to functions.')

    return obj


globs = {
    '__builtins__': dict(i for dct in [safe_builtins, limited_builtins] for i in dct.items()),
    # '__builtins__': __builtins__.__dict__.copy(),
    '__name__': '__main__'
    }

globs['__builtins__']['print'] = print
globs['__builtins__']['super'] = super


exec(code, globs)
