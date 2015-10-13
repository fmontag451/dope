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

import functools
import inspect

from .error import InjectError
from .value import Getter

__all__ = (
    'inject',
)


def inject(**inject_kwargs):
    def inject_decorator(func):
        _sig = inspect.signature(func)
        _inj_kwargs = {}
        for arg_name, arg_value in inject_kwargs.items():
            if arg_name in _sig.parameters:
                if not isinstance(arg_value, Getter):
                    raise InjectError("invalid argument {!r}".format(arg_value))
            else:
                raise InjectError("cannot inject parameter {} to function {}".format(arg_name, func.__name__))
            _inj_kwargs[arg_name] = arg_value

        @functools.wraps(func)
        def wrap(*args, **kwargs):
            bound_args = _sig.bind_partial(*args, **kwargs)
            unbound_args = set(_sig.parameters).difference(bound_args.arguments)
            fill_args = []
            fill_kwargs = {}
            for arg_name in unbound_args:
                param = _sig.parameters[arg_name]
                if param.kind == param.POSITIONAL_ONLY:
                    fill_args.append(_inj_kwargs[arg_name]())
                else:
                    fill_kwargs[arg_name] = _inj_kwargs[arg_name]()
            call_args = bound_args.args
            if fill_args:
                call_args += tuple(fill_args)
            call_kwargs = bound_args.kwargs
            if fill_kwargs:
                call_kwargs.update(fill_kwargs)
            return func(*call_args, **call_kwargs)
            # py3.5:
            # argdict = {arg: inject_args[arg]() for arg in unbound_args}
            # bound_args.apply_defaults(**argdict)
            # return func(*bound_args.args, **bound_args.kwargs)

        return wrap

    return inject_decorator
