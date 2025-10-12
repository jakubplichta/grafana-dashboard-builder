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
from grafana_dashboards.common import get_component_type
from grafana_dashboards.components.axes import Yaxes
from grafana_dashboards.components.base import JsonListGenerator, JsonGenerator
from grafana_dashboards.components.links import Links
from grafana_dashboards.components.targets import Targets

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class Panels(JsonListGenerator):
    def __init__(self, data, registry):
        super().__init__(data, registry, PanelsItemBase)


class PanelsItemBase(JsonGenerator):
    _default_span = None

    def __init__(self, data, registry):
        super().__init__(data, registry)
        self._register_copy_fields({
            'description', 'transparent', 'repeat', ('span', self._default_span), ('title', None)
        })


class Graph(PanelsItemBase):
    _default_span = 12

    def __init__(self, data, registry):
        super().__init__(data, registry)
        self._register_copy_fields({
            'stack', 'fill', 'aliasColors', 'leftYAxisLabel', 'bars', 'lines', 'linewidth', 'y_formats',
            'x-axis', 'y-axis', 'points', 'pointradius', 'percentage', 'steppedLine',
            'repeatDirection', 'decimals', 'minSpan', 'datasource'
        })

    def gen_json_from_data(self, data, context):
        panel_json = super().gen_json_from_data(data, context)
        panel_json.update({
            'type': 'graph',
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
                'rightSide': self.data['legend'].get('rightSide', False),
                'hideEmpty': self.data['legend'].get('hideEmpty', False),
                'hideZero': self.data['legend'].get('hideZero', False),
                'sideWidth': self.data['legend'].get('sideWidth', None)
            }
        if 'tooltip' in self.data:
            panel_json['tooltip'] = {
                'value_type': self.data['tooltip'].get('value_type', 'individual'),
                'shared': self.data['tooltip'].get('shared', False),
                'sort': self.data['tooltip'].get('sort', 0),
            }
        if 'seriesOverrides' in self.data:
            overrides = []
            for override in self.data['seriesOverrides']:
                for alias, settings in override.items():
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
    def __init__(self, data, registry):
        super().__init__(data, registry)
        self._register_copy_fields({
            'prefix', 'postfix', 'nullText', 'format', 'thresholds', 'colorValue', 'colorBackground',
            'colors', 'prefixFontSize', 'valueFontSize', 'postfixFontSize', 'maxDataPoints', 'datasource',
            'repeatDirection', 'decimals', 'minSpan', 'colorPostfix'
        })

    def gen_json_from_data(self, data, context):
        panel_json = super().gen_json_from_data(data, context)
        panel_json.update({
            'type': 'singlestat',
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
        if 'gauge' in data:
            panel_json['gauge'] = {
                'show': True,
                'minValue': data['gauge'].get('minValue', 0),
                'maxValue': data['gauge'].get('maxValue', 100),
                'thresholdMarkers': data['gauge'].get('thresholdMarkers', True),
                'thresholdLabels': data['gauge'].get('thresholdLabels', False)
            }
        if 'colors' not in data:
            panel_json['colors'] = [
                'rgba(50, 172, 45, 0.97)',
                'rgba(237, 129, 40, 0.89)',
                'rgba(245, 54, 54, 0.9)'
            ]
        if 'valueMaps' in data:
            panel_json['valueMaps'] = [{'value': value, 'op': '=', 'text': text} for value, text in
                                       data['valueMaps'].items()]
        if get_component_type(Links) in data:
            panel_json['links'] = self.registry.create_component(Links, data).gen_json()
        return panel_json


class Table(PanelsItemBase):
    def __init__(self, data, registry):
        super().__init__(data, registry)
        self._register_copy_fields({
            'fontSize', 'pageSize', 'showHeader', 'scroll', 'datasource'
        })

    def gen_json_from_data(self, data, context):
        panel_json = super().gen_json_from_data(data, context)
        panel_json.update({
            'type': 'table',
            'targets': [{'target': v} for v in data.get('targets', [])],
            'transform': data.get('transform', None),
            'columns': [{'text': v, 'value': str(v).lower()} for v in data.get('columns', [])]
        })
        panel_json['targets'] = self.registry.create_component(Targets, data).gen_json() if 'targets' in data else []

        if 'styles' in self.data:
            styles = []
            for override in self.data['styles']:
                for pattern, settings in override.items():
                    to_add = {'pattern': pattern}
                    to_add.update(settings)
                    styles.append(to_add)
            panel_json['styles'] = styles

        return panel_json


class Text(PanelsItemBase):

    def gen_json_from_data(self, data, context):
        panel_json = super().gen_json_from_data(data, context)
        panel_json.update({
            'type': 'text',
            'mode': data.get('mode', 'text'),
            'content': data.get('content', '')
        })
        return panel_json


class Dashlist(PanelsItemBase):
    _default_span = 12

    def __init__(self, data, registry):
        super().__init__(data, registry)
        self._register_copy_fields({
            'headings', 'limit', 'recent', 'tags', 'query'
        })

    def gen_json_from_data(self, data, context):
        panel_json = super().gen_json_from_data(data, context)
        panel_json.update({
            'type': 'dashlist',
            'search': 'query' in data or 'tags' in data,
            'starred': data.get('starred') or ('query' not in data and 'tags' not in data)
        })
        return panel_json


class Gauge(PanelsItemBase):
    _default_span = 12

    def __init__(self, data, registry):
        super().__init__(data, registry)
        self._register_copy_fields({
            'datasource', 'pluginVersion'
        })

    def gen_json_from_data(self, data, context):
        panel_json = super().gen_json_from_data(data, context)
        panel_json.update({
            'type': 'gauge',
            'timeFrom': data.get('timeFrom', None),
            'timeShift': data.get('timeShift', None)
        })
        panel_json['targets'] = self.registry.create_component(Targets, data).gen_json() if 'targets' in data else []
        options_data = self.data.get('options', {}) or {}
        field_options_data = options_data.get('fieldOptions', {}) or {}
        field_options = {
            'values': field_options_data.get('values', False),
            'calcs': field_options_data.get('calcs', ['mean']),
            'defaults': field_options_data.get('defaults',
                                               {'mappings': [], 'thresholds': {'mode': 'absolute', 'steps': []}}),
            'overrides': field_options_data.get('overrides', [])
        }
        panel_json['options'] = {
            'showThresholdMarkers': options_data.get('showThresholdMarkers', False),
            'showThresholdLabels': options_data.get('showThresholdLabels', False),
            'orientation': options_data.get('orientation', 'auto'),
            'fieldOptions': field_options
        }
        return panel_json


class Stat(PanelsItemBase):
    _default_span = 12

    def __init__(self, data, registry):
        super().__init__(data, registry)
        self._register_copy_fields({
            'datasource', 'pluginVersion'
        })

    def gen_json_from_data(self, data, context):
        panel_json = super().gen_json_from_data(data, context)
        panel_json.update({
            'type': 'stat',
            'timeFrom': data.get('timeFrom', None),
            'timeShift': data.get('timeShift', None),
            'maxDataPoints': data.get('maxDataPoints', None)
        })
        panel_json['targets'] = self.registry.create_component(Targets, data).gen_json() if 'targets' in data else []

        config_data = self.data.get('fieldConfig', {}) or {}
        defaults_data = config_data.get('defaults', {}) or {}
        defaults = {
            'color': defaults_data.get('color', {'mode': 'thresholds'}),
            'mappings': defaults_data.get('mappings', []),
            'thresholds': defaults_data.get('thresholds', {'mode': 'absolute', 'steps': []}),
            'unit': defaults_data.get('unit', 'percent')
        }
        overrides = config_data.get('overrides', [])
        panel_json['fieldConfig'] = {
            'defaults': defaults,
            'overrides': overrides
        }

        options_data = self.data.get('options', {}) or {}
        field_options_data = options_data.get('fieldOptions', {}) or {}
        field_options = {
            'values': field_options_data.get('values', False),
            'calcs': field_options_data.get('calcs', ['mean']),
            'defaults': field_options_data.get('defaults',
                                               {'mappings': [], 'thresholds': {'mode': 'absolute', 'steps': []}}),
            'overrides': field_options_data.get('overrides', [])
        }
        reduce_options_data = options_data.get('reduceOptions', {}) or {}
        reduce_options = {
            'calcs': reduce_options_data.get('calcs', ['mean']),
            'fields': reduce_options_data.get('fields', ''),
            'values': reduce_options_data.get('values', False)
        }
        panel_json['options'] = {
            'graphMode': options_data.get('graphMode', 'area'),
            'colorMode': options_data.get('colorMode', 'value'),
            'justifyMode': options_data.get('justifyMode', 'auto'),
            'orientation': options_data.get('orientation', 'auto'),
            'fieldOptions': field_options,
            'reduceOptions': reduce_options
        }
        return panel_json


class BarGauge(PanelsItemBase):
    _default_span = 12

    def __init__(self, data, registry):
        super().__init__(data, registry)
        self._register_copy_fields({'datasource'})

    def gen_json_from_data(self, data, context):
        panel_json = super().gen_json_from_data(data, context)

        panel_json.update({
            'type': 'bargauge',
            'timeFrom': data.get('timeFrom', None),
            'timeShift': data.get('timeShift', None)
        })
        panel_json['targets'] = self.registry.create_component(Targets, data).gen_json() if 'targets' in data else []
        options_data = self.data.get('options', {}) or {}
        field_options_data = options_data.get('fieldOptions', {}) or {}
        field_options = {
            'values': field_options_data.get('values', False),
            'calcs': field_options_data.get('calcs', ['last']),
            'defaults': field_options_data.get('defaults', None),
            'mappings': field_options_data.get('mappings', []),
            'thresholds': field_options_data.get('thresholds', []),
            'override': field_options_data.get('override', None)
        }
        panel_json['options'] = {
            'orientation': options_data.get('orientation', 'auto'),
            'displayMode': options_data.get('displayMode', 'lcd'),
            'fieldOptions': field_options
        }
        return panel_json
