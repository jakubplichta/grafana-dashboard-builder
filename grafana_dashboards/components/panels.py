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
        if 'y_formats' in self.data:
            panel_json['y_formats'] = self.data['y_formats']
        if 'grid' in self.data:
            panel_json['grid'] = {
                'leftMax': self.data['grid'].get('leftMax', None),
                'rightMax': self.data['grid'].get('rightMax', None),
                'leftMin': self.data['grid'].get('leftMin', None),
                'rightMin': self.data['grid'].get('rightMin', None)
            }
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
