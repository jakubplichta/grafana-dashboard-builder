# -*- coding: utf-8 -*-
# Copyright 2015-2018 grafana-dashboard-builder contributors
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
from grafana_dashboards.common import get_component_type
from grafana_dashboards.components.base import JsonListGenerator, JsonGenerator
from grafana_dashboards.errors import UnregisteredComponentError

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class Targets(JsonListGenerator):
    def __init__(self, data, registry):
        super(Targets, self).__init__(data, registry, TargetsItemBase)

    def gen_item_json(self, items, result_list):
        try:
            super(Targets, self).gen_item_json(items, result_list)
        except UnregisteredComponentError:
            result_list.append(
                self.registry.create_component(GraphiteTarget, {get_component_type(GraphiteTarget): items}).gen_json()
            )


class TargetsItemBase(JsonGenerator):
    pass


class GraphiteTarget(TargetsItemBase):

    def gen_json_from_data(self, data, context):
        template_json = super(GraphiteTarget, self).gen_json_from_data(data, context)
        if isinstance(data, str):
            template_json['target'] = data
        else:
            template_json['target'] = data['target']
        return template_json


class PrometheusTarget(TargetsItemBase):
    _copy_fields = {'format', 'hide', 'intervalFactor', 'legendFormat', 'step'}

    def gen_json_from_data(self, data, context):
        template_json = super(PrometheusTarget, self).gen_json_from_data(data, context)
        template_json['expr'] = data['expr']
        return template_json


class InfluxdbTarget(TargetsItemBase):
    _copy_fields = {'alias'}

    def gen_json_from_data(self, data, context):
        template_json = super(InfluxdbTarget, self).gen_json_from_data(data, context)
        template_json['query'] = data['query']
        template_json['dsType'] = 'influxdb'
        template_json['rawQuery'] = True
        return template_json
