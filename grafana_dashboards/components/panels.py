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
from grafana_dashboards.components.base import JsonListGenerator, JsonGenerator
from grafana_dashboards.common import get_component_type
from grafana_dashboards.components.links import Links

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class Panels(JsonListGenerator):
    def __init__(self, data, registry):
        super(Panels, self).__init__(data, registry, PanelsItemBase)


class PanelsItemBase(JsonGenerator):
    pass


class Graph(PanelsItemBase):
    def gen_json_from_data(self, data, context):
        panel_json = {
            'type': 'graph',
            'title': self.data.get('title', None),
            'span': self.data.get('span', None),
        }
        targets = self.data.get('targets', [])
        if 'target' in self.data:
            targets.append(self.data['target'])
        panel_json['targets'] = map(lambda v: {'target': v}, targets)
        panel_json['nullPointMode'] = self.data.get('nullPointMode', 'null')
        if 'stack' in self.data:
            panel_json['stack'] = self.data['stack']
        if 'fill' in self.data:
            panel_json['fill'] = self.data['fill']
        if 'aliasColors' in self.data:
            panel_json['aliasColors'] = self.data['aliasColors']
        if 'leftYAxisLabel' in self.data:
            panel_json['leftYAxisLabel'] = self.data['leftYAxisLabel']
        if 'bars' in self.data:
            panel_json['bars'] = self.data['bars']
        if 'lines' in self.data:
            panel_json['lines'] = self.data['lines']
        if 'y_formats' in self.data:
            panel_json['y_formats'] = self.data['y_formats']
        if 'grid' in self.data:
            panel_json['grid'] = {
                'leftMax': self.data['grid'].get('leftMax', None),
                'rightMax': self.data['grid'].get('rightMax', None),
                'leftMin': self.data['grid'].get('leftMin', None),
                'rightMin': self.data['grid'].get('rightMin', None)
            }
        if 'legend' in self.data:
            panel_json['legend'] = {
                'show': self.data['legend'].get('show', True),
                'values': self.data['legend'].get('values', False),
                'min': self.data['legend'].get('min', False),
                'max': self.data['legend'].get('max', False),
                'current': self.data['legend'].get('current', False),
                'total': self.data['legend'].get('total', False),
                'avg': self.data['legend'].get('avg', False),
                'alignAsTable': self.data['legend'].get('alignAsTable', False),
                'hideEmpty': self.data['legend'].get('hideEmpty', False)
            }
        if get_component_type(Links) in self.data:
            panel_json['links'] = self.registry.create_component(Links, self.data).gen_json()
        return panel_json


class SingleStat(PanelsItemBase):
    def gen_json_from_data(self, data, context):
        panel_json = {
            'type': 'singlestat',
            'title': self.data.get('title', None),
            'span': self.data.get('span', None),
            'targets': map(lambda v: {'target': v}, self.data.get('targets', [])),
            'nullPointMode': self.data.get('nullPointMode', 'null'),
            'valueName': self.data.get('valueName', 'current')
        }
        if 'prefix' in self.data:
            panel_json['prefix'] = self.data['prefix']
        if 'postfix' in self.data:
            panel_json['postfix'] = self.data['postfix']
        if 'nullText' in self.data:
            panel_json['nullText'] = self.data['nullText']
        if 'format' in self.data:
            panel_json['format'] = self.data['format']
        if 'sparkline' in self.data:
            panel_json['sparkline'] = {
                'show': True,
                'full': self.data['sparkline'].get('full', False),
                'lineColor': self.data['sparkline'].get('lineColor', 'rgb(31, 120, 193)'),
                'fillColor': self.data['sparkline'].get('fillColor', 'rgba(31, 118, 189, 0.18)')
            }
        if get_component_type(Links) in self.data:
            panel_json['links'] = self.registry.create_component(Links, self.data).gen_json()
        return panel_json


class Text(PanelsItemBase):
    def gen_json_from_data(self, data, context):
        return {
            'type': 'text',
            'title': self.data.get('title', None),
            'span': self.data.get('span', None),
            'mode': self.data.get('mode', 'text'),
            'content': self.data.get('content', '')
        }
