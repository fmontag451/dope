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

import pytest

import dope


# TODO: add multiple injectors fixture

@pytest.fixture
def config():
    return dope.Injector(
        attr_dependency_1="ATTR_1",
        configured_attribute_2="ATTR_2",
        dependency_1="DEP_1",
        dependency_2="DEP_1",
    )


class TestClass(object):

    attr_dependency_1 = dope.Key()  # retrieve key directly from attribute name

    attr_dependency_2 = dope.Key("configured_attribute_2")  # explicit key

    @dope.register(dependency_1=dope.Key(), dependency_2=dope.Key())
    def __init__(self, arg1, arg2, dependency_1, dependency_2):
        self.dependency_1 = dependency_1
        self.dependency_2 = dependency_2

    def __repr__(self):
        return "<{}: dependency_1={!r}, dependency_2={!r}, attr_dependency_1={!r}, attr_dependency_2={!r}".format(
            self.__class__.__name__,
            self.dependency_1, self.dependency_2,
            self.attr_dependency_1, self.attr_dependency_2,
        )


def test_injection(config):
    inst = config.get(TestClass, arg1='arg1', arg2='arg2')
    assert isinstance(inst, TestClass)
    # Check constructor injection
    assert config['dependency_1'] == inst.dependency_1
    assert config['dependency_2'] == inst.dependency_2
    # Check attributes injection
    assert config['attr_dependency_1'] == inst.attr_dependency_1
    assert config['configured_attribute_2'] == inst.attr_dependency_2
