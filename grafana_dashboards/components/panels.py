# -*- coding: utf-8 -*-
# Copyright 2015-2016 grafana-dashboard-builder contributors
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

    # noinspection PySetFunctionToLiteral
    _copy_fields = set(['stack', 'fill', 'aliasColors', 'leftYAxisLabel', 'bars', 'lines', 'linewidth', 'y_formats',
                        'x-axis', 'y-axis', 'xaxis', 'yaxes'])

    def gen_json_from_data(self, data, context):
        panel_json = super(Graph, self).gen_json_from_data(data, context)
        panel_json.update({
            'type': 'graph',
            'title': self.data.get('title', None),
            'span': self.data.get('span', None),
        })
        targets = self.data.get('targets', [])
        if 'target' in self.data:
            targets.append(self.data['target'])
        panel_json['targets'] = map(lambda v: {'target': v}, targets)
        panel_json['nullPointMode'] = self.data.get('nullPointMode', 'null')
        if 'grid' in self.data:
            panel_json['grid'] = {
                'leftMax': self.data['grid'].get('leftMax', None),
                'rightMax': self.data['grid'].get('rightMax', None),
                'leftMin': self.data['grid'].get('leftMin', None),
                'rightMin': self.data['grid'].get('rightMin', None),
                'threshold1': self.data['grid'].get('threshold1', None),
                'threshold2': self.data['grid'].get('threshold2', None)
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
        if 'tooltip' in self.data:
            panel_json['tooltip'] = {
                'value_type': self.data['tooltip'].get('value_type', 'individual'),
                'shared': self.data['tooltip'].get('shared', False),
            }
        if 'seriesOverrides' in self.data:
            overrides = []
            for override in self.data['seriesOverrides']:
                for alias, settings in override.iteritems():
                    to_add = {'alias': alias}
                    to_add.update(settings)
                    overrides.append(to_add)
            panel_json['seriesOverrides'] = overrides
        if get_component_type(Links) in self.data:
            panel_json['links'] = self.registry.create_component(Links, self.data).gen_json()
        return panel_json


class SingleStat(PanelsItemBase):

    # noinspection PySetFunctionToLiteral
    _copy_fields = set(['prefix', 'postfix', 'nullText', 'format', 'thresholds', 'colorValue', 'colorBackground',
                        'colors', 'prefixFontSize', 'valueFontSize', 'postfixFontSize', 'maxDataPoints'])

    def gen_json_from_data(self, data, context):
        panel_json = super(SingleStat, self).gen_json_from_data(data, context)
        panel_json.update({
            'type': 'singlestat',
            'title': data.get('title', None),
            'span': data.get('span', None),
            'targets': map(lambda v: {'target': v}, data.get('targets', [])),
            'nullPointMode': data.get('nullPointMode', 'null'),
            'valueName': data.get('valueName', 'current')
        })
        if 'sparkline' in data:
            panel_json['sparkline'] = {
                'show': True,
                'full': data['sparkline'].get('full', False),
                'lineColor': data['sparkline'].get('lineColor', 'rgb(31, 120, 193)'),
                'fillColor': data['sparkline'].get('fillColor', 'rgba(31, 118, 189, 0.18)')
            }
        if 'colors' not in data:
            panel_json['colors'] = [
                'rgba(50, 172, 45, 0.97)',
                'rgba(237, 129, 40, 0.89)',
                'rgba(245, 54, 54, 0.9)'
            ]
        if 'valueMaps' in data:
            panel_json['valueMaps'] = [{'value': value, 'op': '=', 'text': text} for value, text in
                                       data['valueMaps'].iteritems()]
        if get_component_type(Links) in data:
            panel_json['links'] = self.registry.create_component(Links, data).gen_json()
        return panel_json


class Table(PanelsItemBase):
    # noinspection PySetFunctionToLiteral
    _copy_fields = set(['fontSize', 'pageSize', 'showHeader', 'scroll'])

    def gen_json_from_data(self, data, context):
        panel_json = super(Table, self).gen_json_from_data(data, context)
        panel_json.update({
            'type': 'table',
            'title': data.get('title', None),
            'span': data.get('span', None),
            'targets': map(lambda v: {'target': v}, data.get('targets', [])),
            'transform': data.get('transform', None),
            'columns': map(lambda v: {'text': v, 'value': str(v).lower()}, data.get('columns', []))
        })

        if 'styles' in self.data:
            styles = []
            for override in self.data['styles']:
                for pattern, settings in override.iteritems():
                    to_add = {'pattern': pattern}
                    to_add.update(settings)
                    styles.append(to_add)
            panel_json['styles'] = styles

        return panel_json


class Text(PanelsItemBase):
    def gen_json_from_data(self, data, context):
        panel_json = super(Text, self).gen_json_from_data(data, context)
        panel_json.update({
            'type': 'text',
            'title': data.get('title', None),
            'span': data.get('span', None),
            'mode': data.get('mode', 'text'),
            'content': data.get('content', '')
        })
        return panel_json
