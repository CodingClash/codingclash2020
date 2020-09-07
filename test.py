class FrozenClass(object):
    __isfrozen = False
    def __setattr__(self, key, value):
        if self.__isfrozen and not hasattr(self, key):
            raise TypeError( "%r is a frozen class" % self )
        object.__setattr__(self, key, value)

    def _freeze(self):
        self.__isfrozen = True


from functools import wraps

def froze_it(cls):
    cls.__frozen = False

    def frozensetattr(self, key, value):
        if self.__frozen and not hasattr(self, key):
            print("Class {} is frozen. Cannot set {} = {}"
                  .format(cls.__name__, key, value))
        else:
            object.__setattr__(self, key, value)

    def init_decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.__frozen = True
        return wrapper

    cls.__setattr__ = frozensetattr
    cls.__init__ = init_decorator(cls.__init__)

    return cls

from enum import Enum

@froze_it
class Thing(Enum):
    ONE = 1
    TWO = 2


# class Test(FrozenClass):
#     def __init__(self):
#         self.x = 42#
#         self.y = 2**3

#         self._freeze() # no new attributes after this point.

# a,b = Test(), Test()
# a.x = 10
# b.z = 10 # fails

Thing.THREE = 4
print(Thing.THREE)