# -*- coding: utf-8 -*-
#
# Copyright 2015 Simone Campagna
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections

from .value import Value, Instance, Getter

__all__ = (
    'Trove',
    'DeferredTrove',
)


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
