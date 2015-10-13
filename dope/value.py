__all__ = (
    'Value',
    'Instance',
    'Factory',
    'Getter',
)

import abc


class Value(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self):
         raise NotImplementedError()


class Instance(Value):
    def __init__(self, value):
         self._value = value

    def __call__(self):
         return self._value

    
class Factory(Value):
    def __init__(self, func):
         self._func = func

    def __call__(self):
        return self._func()


class Getter(Value):
    def __init__(self, trove, key):
         self._trove = trove
         self._key = key

    def __call__(self):
         return self._trove[self._key]()
