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
from __future__ import annotations

import logging
import string
import uuid
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from typing import Any, TypeVar

from grafana_dashboards import errors
from grafana_dashboards.common import get_component_type
from grafana_dashboards.context import Context

T = TypeVar('T', bound='ComponentBase')

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'

logger = logging.getLogger(__name__)


def get_generators() -> list[type]:
    return _get_subclasses(JsonGenerator)


def _get_subclasses(clazz: type) -> list[type]:
    direct_subclasses = clazz.__subclasses__()
    return [sub for sub in
            direct_subclasses + [sub_class for direct in direct_subclasses for sub_class in _get_subclasses(direct)]
            if sub not in (ComponentBase, JsonGenerator, JsonListGenerator)]


def get_placeholders(component_name: str) -> list[str]:
    return [v[1] for v in string.Formatter().parse(component_name) if v[1]]


class ComponentRegistry:
    _components: dict[type, dict[str, ComponentBase]]

    def __init__(self) -> None:
        super().__init__()
        self._types: dict[str, type] = {}
        self._components: dict[type, dict[str, ComponentBase]] = {}
        for clazz in _get_subclasses(ComponentBase):
            logger.info('Loading component type %s', clazz)
            self._types[get_component_type(clazz)] = clazz
            self._components[clazz] = {}

    def _class_for_type(self, component_type: str | type[T] | None) -> type[T]:
        if isinstance(component_type, str):
            component_type = self._types.get(component_type)
        if component_type is None:
            raise errors.UnregisteredComponentError(f"No component of type '{component_type}' found!")
        if self._components.get(component_type) is None:
            raise errors.UnregisteredComponentError(f"No component of type '{component_type}' found!")
        return component_type

    def add(self, component: dict[str, Any]) -> None:
        if len(component) > 2:
            raise errors.WrongComponentAttributeCountError(
                f'Component must have exactly 2 attributes - name and component type with data.'
                f'This contains {len(component.keys())} attributes')
        component_name = component.get('name')
        if component_name is None:
            logger.info("Component '%s' does not have 'name' attribute, skipping", component.keys())
            return
        component_type = None
        for key in component.keys():
            if key == 'name':
                continue
            component_type = key
            break
        try:
            clazz: type[ComponentBase] = self._class_for_type(component_type)
        except errors.UnregisteredComponentError:
            logger.info("Missing implementation class for component '%s', skipping", component_type)
            return
        logger.debug("Adding component '%s' with name '%s'", component_type, component_name)
        components = self._get_component(clazz)
        if component_name in components:
            raise errors.DuplicateKeyError(
                f"Key '{component_name}' is already defined for component {component_type}")
        components[component_name] = self.create_component(clazz, component)

    def __getitem__(self, item: type[T]) -> Iterable[T]:
        return self._get_component(item).values()

    def _get_component(self, item: type[T]) -> dict[str, T]:
        component: dict[str, T] | None = self._components.get(item)  # type: ignore
        if component is None:
            raise errors.UnregisteredComponentError(f"No component of type '{item}' found!")
        return component

    def create_component(self, component_type: str | type[T] | None, data: dict[str, Any]) -> T:
        return self._class_for_type(component_type)(data, self)

    def get_component(self, component_type: type[T], name: str) -> T:
        component = self._get_component(component_type).get(name)
        if component is None:
            raise errors.UnregisteredComponentError(f"No component '{component_type}' with name '{name}' found!")
        return component


class ComponentBase:
    name: str

    def __init__(self, data: dict[str, Any], registry: ComponentRegistry) -> None:
        super().__init__()
        self.data = data[get_component_type(type(self))]
        if self.data is None:
            self.data = {}
        self.name = data.get('name', str(uuid.uuid4()))
        self.registry = registry


class JsonGenerator(ComponentBase, metaclass=ABCMeta):
    _copy_fields: set[str | tuple[str, Any | None]] = set()

    def _register_copy_fields(self, copy_fields: set[str | tuple[str, Any | None]]) -> None:
        self._copy_fields = self._copy_fields.union(copy_fields)

    def gen_json(self, context: Context | None = None) -> Any:
        if context is None:
            context = Context()
        return self.gen_json_from_data(context.expand_placeholders(self.data), context)

    @abstractmethod
    def gen_json_from_data(self, data: Any, context: Context) -> Any:
        pass


class ObjectJsonGenerator(JsonGenerator):
    def gen_json_from_data(self, data: dict[str, Any], context: Context) -> Any:
        component_type = get_component_type(type(self))
        if self.name:
            logger.debug("Processing component '%s' with name '%s' from template '%s'",
                         component_type, context.expand_placeholders(self.name), self.name)
        else:
            logger.debug("Processing anonymous component '%s'", component_type)
        json = {}
        for field in self._copy_fields:
            if isinstance(field, tuple):
                field_key = field[0]
                field_default = field[1]
                json[field_key] = data.get(field_key, field_default)
            elif field in data:
                json[field] = data[field]
        return json


class JsonListGenerator(JsonGenerator):
    def __init__(self, data: Any, registry: ComponentRegistry, item_base_classes: list[type]) -> None:
        super().__init__(data, registry)
        self.component_item_types = [
            get_component_type(clazz)
            for item_base_class in item_base_classes
            for clazz in _get_subclasses(item_base_class)
        ]

    def gen_json_from_data(self, data: Any, context: Context) -> list[Any]:
        result_list: list[Any] = []
        for items in data:
            self.gen_item_json(items, result_list)
        return result_list

    def gen_item_json(self, items: str | dict[str, Any], result_list: list[Any]) -> None:
        if isinstance(items, str):
            # this is component without context
            result_list += self.registry.get_component(type(self), items).gen_json()
        else:
            self._gen_item_json_with_context(items, result_list)

    def _gen_item_json_with_context(self, items: dict[str, Any], result_list: list[Any]) -> None:
        # TODO add check for dictionary
        for (item_type, item_data) in items.items():
            if item_type not in self.component_item_types:
                # this is named component with context
                for context in Context.create_context(item_data, get_placeholders(item_type)):
                    result_list += self.registry.get_component(type(self), item_type).gen_json(context)
            else:
                # this is inplace defined component
                item: Any = self.registry.create_component(item_type, {item_type: item_data}).gen_json()
                if isinstance(item, list):
                    result_list += item
                else:
                    result_list.append(item)
