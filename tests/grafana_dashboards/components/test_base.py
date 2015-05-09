# -*- coding: utf-8 -*-
# Copyright 2015 grafana-dashboard-builder contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from grafana_dashboards.components.base import ComponentRegistry, ComponentBase
from grafana_dashboards.errors import UnregisteredComponentError, MissingComponentNameError, DuplicateKeyError, \
    WrongComponentAttributeCountError

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class TestBase(ComponentBase):
    pass


def test_registry():
    registry = ComponentRegistry()

    with pytest.raises(UnregisteredComponentError):
        registry.add({'name': 'name', 'non-existent': {}})
        registry.get_component('non-existent', 'name')

    registry.add({})
    with pytest.raises(WrongComponentAttributeCountError):
        registry.add({'test-base': {}})

    with pytest.raises(WrongComponentAttributeCountError):
        registry.add({'test-base': {}, 'other': '', 'yet-another': ''})

    with pytest.raises(MissingComponentNameError):
        registry.add({'test-base': {}, 'other': ''})

    registry.add({'name': 'name', 'test-base': {}})
    assert registry.get_component(TestBase, 'name') is not None
    assert registry[TestBase] is not None

    with pytest.raises(DuplicateKeyError):
        registry.add({'name': 'name', 'test-base': {}})
