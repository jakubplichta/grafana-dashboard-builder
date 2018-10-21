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
from grafana_dashboards.components.annotations import Annotations
from grafana_dashboards.components.base import JsonGenerator
from grafana_dashboards.common import get_component_type
from grafana_dashboards.components.rows import Rows
from grafana_dashboards.components.templates import Templates

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class Dashboard(JsonGenerator):

    # noinspection PySetFunctionToLiteral
    _copy_fields = set(['sharedCrosshair'])

    def gen_json_from_data(self, data, context):
        json_data = super(Dashboard, self).gen_json_from_data(data, context)
        nav = {
            'type': 'timepicker'
        }
        json_data.update({
            'title': data.get('title', self.name),
            'nav': [
                nav
            ]
        })
        if 'time' in data:
            json_data['time'] = {
                'from': data['time']['from'],
                'to': data['time']['to']
            }
        if 'tags' in data:
            json_data['tags'] = data.get('tags')
        if 'time_options' in data:
            nav['time_options'] = data.get('time_options', [])
        if 'refresh_intervals' in data:
            nav['refresh_intervals'] = data.get('refresh_intervals', [])
        if 'refresh' in data:
            json_data['refresh'] = data.get('refresh')
        if get_component_type(Annotations) in data:
            json_data['annotations'] = {'list': self.registry.create_component(Annotations, data).gen_json()}
        if get_component_type(Rows) in data:
            json_data['rows'] = self.registry.create_component(Rows, data).gen_json()
        if get_component_type(Templates) in data:
            json_data['templating'] = {
                'list': self.registry.create_component(Templates, data).gen_json(),
                'enable': True
            }
        return json_data
