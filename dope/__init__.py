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
