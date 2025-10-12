# Copyright 2015-2025 grafana-dashboard-builder contributors
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

from grafana_dashboards import errors
from grafana_dashboards.components.base import ComponentRegistry, ComponentBase

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class TestBase(ComponentBase):
    __test__ = False


def test_registry_unregistered_component():
    registry = ComponentRegistry()

    registry.add({'name': 'name', 'non-existent': {}})
    with pytest.raises(errors.UnregisteredComponentError):
        registry.get_component('non-existent', 'name')


def test_registry_add_ignored():
    registry = ComponentRegistry()

    registry.add({})


def test_registry_add_component_with_too_few_fields():
    registry = ComponentRegistry()

    registry.add({'test-base': {}})
    with pytest.raises(errors.UnregisteredComponentError):
        registry.get_component('test-base', None)


def test_registry_add_component_with_too_many_fields():
    registry = ComponentRegistry()

    with pytest.raises(errors.WrongComponentAttributeCountError):
        registry.add({'test-base': {}, 'other': '', 'yet-another': ''})


def test_registry_add_component_without_name():
    registry = ComponentRegistry()

    registry.add({'test-base': {}, 'other': ''})
    with pytest.raises(errors.UnregisteredComponentError):
        registry.get_component('test-base', None)


def test_registry_add_component():
    registry = ComponentRegistry()

    registry.add({'name': 'name', 'test-base': {}})
    assert registry.get_component(TestBase, 'name') is not None
    assert registry[TestBase] is not None


def test_registry_add_component_duplicate_key():
    registry = ComponentRegistry()

    registry.add({'name': 'name', 'test-base': {}})
    with pytest.raises(errors.DuplicateKeyError):
        registry.add({'name': 'name', 'test-base': {}})
