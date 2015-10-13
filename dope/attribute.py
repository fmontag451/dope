# -*- coding: utf-8 -*-
#
# Copyright 2015 Federico Ficarelli
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

__all__ = (
    'attr',
)


def attr(value):
    return InjectedAttribute(value)


class InjectedAttribute(object):
    def __init__(self, value):
        self._value = value

    def __get__(self, instance, owner):
        """ Enables data descriptor semantics on injected attributes. """
        pass

    def __set__(self, instance, value):  # TODO: do we really need read-only semantics?
        """ Enables data descriptor semantics on injected attributes.

        Raises
        ------
        AttributeError
            To enforce read-only data descriptor semantics.
        """
        raise AttributeError("Can't set attribute")
