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

from . import registry
from .trove import Trove

__all__ = (
    'Injector',
)


class Injector(Trove):
    def __init__(self, *args, **kwargs):
        self._register = registry.register
        super().__init__(*args, **kwargs)

    def get(self, function_or_class, **kwargs):
        args = ()  # positional args are not supported due to the 'self' parameter
        function = registry.get_function(function_or_class)
        data = self._register.get(function, None)
        if data is not None:
            signature, function_injected_args = data
            bound_args = signature.bind_partial(*args, **kwargs)
            unbound_args = set(signature.parameters).difference(bound_args.arguments)
            fill_args = []
            fill_kwargs = {}
            for arg_name in unbound_args:
                if arg_name in function_injected_args:
                    param = signature.parameters[arg_name]
                    instance = self[function_injected_args[arg_name].key]()
                    if param.kind == param.POSITIONAL_ONLY:
                        fill_args.append(instance)
                    else:
                        fill_kwargs[arg_name] = instance
            call_args = bound_args.args
            if fill_args:
                call_args += tuple(fill_args)
            call_kwargs = bound_args.kwargs
            if fill_kwargs:
                call_kwargs.update(fill_kwargs)
        else:
            call_args, call_kwargs = args, kwargs
        # print("call:", call_args, call_kwargs)
        return function_or_class(*call_args, **call_kwargs)
