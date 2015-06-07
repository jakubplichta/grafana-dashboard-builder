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
import logging
import re
import string

from grafana_dashboards.context import Context
from grafana_dashboards.errors import MissingComponentNameError, DuplicateKeyError, UnregisteredComponentError, \
    WrongComponentAttributeCountError

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


logger = logging.getLogger(__name__)

_first_cap_re = re.compile('(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')


def get_component_type(clazz):
    """

    :type clazz: type
    """
    return _all_cap_re.sub(r'\1-\2', _first_cap_re.sub(r'\1-\2', clazz.__name__)).lower()


def get_generators():
    return _get_subclasses(JsonGenerator)


def _get_subclasses(clazz):
    """

    :type clazz: type
    """
    direct_subclasses = clazz.__subclasses__()
    return [sub for sub in
            direct_subclasses + [sub_class for direct in direct_subclasses for sub_class in _get_subclasses(direct)]
            if sub not in (ComponentBase, JsonGenerator, JsonListGenerator)]


def get_placeholders(component_name):
    return [v[1] for v in string.Formatter().parse(component_name) if v[1]]


class ComponentRegistry(object):
    def __init__(self):
        super(ComponentRegistry, self).__init__()
        self._types = {}
        self._components = {}
        for clazz in _get_subclasses(ComponentBase):
            logger.info('Loading component type %s', clazz)
            self._types[get_component_type(clazz)] = clazz
            self._components[clazz] = {}

    def _class_for_type(self, component_type):
        if isinstance(component_type, str):
            component_type = self._types.get(component_type)
        if self._components.get(component_type) is None:
            raise UnregisteredComponentError("No component of type '%s' found!" % component_type)
        return component_type

    def add(self, component):
        """

        :type component: dict
        """
        component_type = None
        for key in component.keys():
            if key == 'name':
                continue
            component_type = key
            break
        try:
            clazz = self._class_for_type(component_type)
        except UnregisteredComponentError:
            logger.info("Missing implementation class for component '%s', skipping", component_type)
            return
        if len(component) != 2:
            raise WrongComponentAttributeCountError(
                'Component must have exactly 2 attributes - name and component type with data %s' % len(
                    component.keys()))
        component_name = component.get('name')
        if component_name is None:
            logger.info("Component '%s' does not have 'name' attribute", component_name)
            raise MissingComponentNameError(
                "Component '%s' must contain 'name' attribute. Component data: %s" % (component_name, component))
        logger.debug("Adding component '%s' with name '%s'", component_type, component_name)
        components = self._get_component(clazz)
        if component_name in components:
            raise DuplicateKeyError(
                "Key '%s' is already defined for component %s" % (component_name, component_type))
        components[component_name] = self.create_component(clazz, component)

    def __getitem__(self, item):
        return self._get_component(item).values()

    def _get_component(self, item):
        component = self._components.get(item)
        if component is None:
            raise UnregisteredComponentError("No component of type '%s' found!" % item)
        return component

    def create_component(self, component_type, data):
        return self._class_for_type(component_type)(data, self)

    def get_component(self, component_type, name):
        component = self._get_component(component_type).get(name)
        if component is None:
            raise UnregisteredComponentError("No component '%s' with name '%s' found!" % (component_type, name))
        return component


class ComponentBase(object):
    def __init__(self, data, registry):
        """

        :type registry: ComponentRegistry
        """
        super(ComponentBase, self).__init__()
        self.data = data[get_component_type(type(self))]
        if self.data is None:
            self.data = {}
        self.name = data.get('name')
        self.registry = registry


class JsonGenerator(ComponentBase):
    def gen_json(self, context=Context()):
        return self.gen_json_from_data(context.expand_placeholders(self.data), context)

    def gen_json_from_data(self, data, context):
        return {}


class JsonListGenerator(JsonGenerator):
    def __init__(self, data, registry, item_base_class):
        super(JsonListGenerator, self).__init__(data, registry)
        self.component_item_types = [get_component_type(clazz) for clazz in _get_subclasses(item_base_class)]

    def gen_json_from_data(self, data, context):
        result_list = []
        for items in data:
            if isinstance(items, str):
                result_list += self.registry.get_component(type(self), items).gen_json()
            else:
                for (item_type, item_data) in items.iteritems():
                    if item_type not in self.component_item_types:
                        for context in Context.create_context(item_data, get_placeholders(item_type)):
                            result_list += self.registry.get_component(type(self), item_type).gen_json(context)
                    else:
                        item = self.registry.create_component(item_type, {item_type: item_data}).gen_json()
                        if isinstance(item, list):
                            result_list += item
                        else:
                            result_list.append(item)
        return result_list
