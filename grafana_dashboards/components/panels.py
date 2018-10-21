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
from grafana_dashboards.components.axes import Yaxes
from grafana_dashboards.components.base import JsonListGenerator, JsonGenerator
from grafana_dashboards.components.links import Links
from grafana_dashboards.components.targets import Targets

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class Panels(JsonListGenerator):
    def __init__(self, data, registry):
        super(Panels, self).__init__(data, registry, PanelsItemBase)


class PanelsItemBase(JsonGenerator):
    pass


class Graph(PanelsItemBase):

    _copy_fields = {'stack', 'fill', 'aliasColors', 'leftYAxisLabel', 'bars', 'lines', 'linewidth', 'y_formats',
                    'x-axis', 'y-axis', 'points', 'pointradius', 'percentage', 'steppedLine', 'repeat',
                    'minSpan', 'datasource'}

    def gen_json_from_data(self, data, context):
        panel_json = super(Graph, self).gen_json_from_data(data, context)
        panel_json.update({
            'type': 'graph',
            'title': self.data.get('title', None),
            'span': self.data.get('span', 12),
        })
        targets = self.data.get('targets', [])
        if 'target' in self.data:
            targets.append(self.data['target'])
        self._create_component(panel_json, Targets, {'targets': targets})
        panel_json['nullPointMode'] = self.data.get('nullPointMode', 'null')
        grid_data = self.data.get('grid', {}) or {}
        if 'grid' in self.data or 'y_formats' in self.data:
            panel_json['grid'] = {
                'leftMax': grid_data.get('leftMax', None),
                'rightMax': grid_data.get('rightMax', None),
                'leftMin': grid_data.get('leftMin', None),
                'rightMin': grid_data.get('rightMin', None),
                'threshold1': grid_data.get('threshold1', None),
                'threshold2': grid_data.get('threshold2', None),
                'threshold1Color': grid_data.get('threshold1Color', 'rgba(216, 200, 27, 0.27)'),
                'threshold2Color': grid_data.get('threshold2Color', 'rgba(234, 112, 112, 0.22)')
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
        self._create_component(panel_json, Links, self.data)
        if (('leftYAxisLabel' in self.data
            or 'grid' in self.data and ('leftMin' in grid_data or 'leftMax' in grid_data))
                and ('y_formats' not in self.data)):
            panel_json['y_formats'] = ['short', 'short']
        panel_json['xaxis'] = self.data.get('xaxis', {'show': True, 'format': 'time'})
        self._create_component(panel_json, Yaxes, self.data)
        return panel_json

    def _create_component(self, panel_json, clazz, data):
        if get_component_type(clazz) in data:
            panel_json[get_component_type(clazz)] = self.registry.create_component(clazz, data).gen_json()


class SingleStat(PanelsItemBase):

    # noinspection PySetFunctionToLiteral
    _copy_fields = set(['prefix', 'postfix', 'nullText', 'format', 'thresholds', 'colorValue', 'colorBackground',
                        'colors', 'prefixFontSize', 'valueFontSize', 'postfixFontSize', 'maxDataPoints', 'datasource'])

    def gen_json_from_data(self, data, context):
        panel_json = super(SingleStat, self).gen_json_from_data(data, context)
        panel_json.update({
            'type': 'singlestat',
            'title': data.get('title', None),
            'span': data.get('span', None),
            'nullPointMode': data.get('nullPointMode', 'null'),
            'valueName': data.get('valueName', 'current')
        })
        panel_json['targets'] = self.registry.create_component(Targets, data).gen_json() if 'targets' in data else []
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
    _copy_fields = set(['fontSize', 'pageSize', 'showHeader', 'scroll', 'datasource'])

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
        panel_json['targets'] = self.registry.create_component(Targets, data).gen_json() if 'targets' in data else []

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


class Dashlist(PanelsItemBase):
    _copy_fields = {'headings', 'limit', 'recent', 'tags', 'query'}

    def gen_json_from_data(self, data, context):
        panel_json = super(Dashlist, self).gen_json_from_data(data, context)
        panel_json.update({
            'type': 'dashlist',
            'title': data.get('title', None),
            'span': data.get('span', 12),
            'search': 'query' in data or 'tags' in data,
            'starred': data.get('starred') or ('query' not in data and 'tags' not in data)
        })
        return panel_json
