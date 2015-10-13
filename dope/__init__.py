"""Dope - dependency injection framework

 >>> @register(y=Key("y_value"))
 ... def function(x, y, z):
 ...     return x + y + z
 ...
 >>> injector = Injector()
 >>> injector['y_value'] = 2
 >>> injector.get(function, x=10, y=20, z=30)
 60
 >>> injector.get(function, x=10, z=30)
 42
 >>>

"""


from .error import *
from .inject import *
from .registry import *
from .trove import *
from .value import *
from .injector import *
