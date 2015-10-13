__all__ = (
    'Trove',
    'DeferredTrove',
)

import collections

from .value import Value, Instance, Getter
    

class Trove(collections.MutableMapping):
    def __init__(self, **kwargs):
        self._dict = {}
        self.update(kwargs)

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        assert isinstance(key, str)
        if not isinstance(value, Value):
            value = Instance(value)
        self._dict[key] = value

    def __delitem__(self, key):
        del self._dict[key]

    def __iter__(self):
        yield from self._dict

    def __len__(self):
        return len(self._dict)


class DeferredTrove(object):
    def __init__(self, **kwargs):
        self._trove = Trove(**kwargs)

    def __setitem__(self, key, value):
        self._trove[key] = value

    def __getitem__(self, key):
        return Getter(self._trove, key)

    def __delitem__(self, key):
        del self._trove[key]

    def __iter__(self):
        yield from self._trove

    def __len__(self):
        return len(self._trove)

