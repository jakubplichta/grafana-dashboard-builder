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
from grafana_dashboards.components.base import JsonListGenerator, JsonGenerator

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class Templates(JsonListGenerator):
    def __init__(self, data, registry):
        super(Templates, self).__init__(data, registry, TemplatesItemBase)


class TemplatesItemBase(JsonGenerator):
    pass


class Query(TemplatesItemBase):

    def gen_json_from_data(self, data, context):
        super(Query, self).gen_json_from_data(data, context)
        processed_parts = []
        queries = []
        if not data.get('query'):
            return queries
        if 'name' in data:
            template_json = {
                'type': 'query',
                'name': data['name'],
                'query': data['query']
            }
            if 'refresh' in data:
                template_json['refresh'] = data['refresh']
            elif 'options' in data:
                template_json['refresh'] = 0
            else:
                template_json['refresh'] = 1
            if 'datasource' in data:
                template_json['datasource'] = data['datasource']
            self._copy_data(template_json, data)
            queries.append(template_json)
        else:
            refresh_only_first = data.get('refresh-only-first', False)
            for query_part in data['query'].split('.'):
                if query_part.startswith('$'):
                    is_first = False if queries else True
                    query = query_part[1:]
                    metric = '*'
                    template_json = {
                        'type': 'query',
                        'refresh_on_load': not refresh_only_first or is_first,
                        'name': query,
                        'refresh': not refresh_only_first or is_first
                    }
                    if 'datasource' in data:
                        template_json['datasource'] = data['datasource']
                    if query in data:
                        query_config = data[query]
                        metric = query_config.get('metric', metric)
                        self._copy_data(template_json, query_config)

                    template_json['query'] = '.'.join(processed_parts + [metric])
                    queries.append(template_json)
                processed_parts.append(query_part)
        return queries

    @staticmethod
    def _copy_data(target, source):
        if 'current' in source:
            current = source['current']
            target['current'] = {
                'text': current,
                'value': current
            }
        if 'options' in source:
            target['options'] = [{'text': option, 'value': option} for option in
                                 (source['options'])]
        for key in ['regex', 'multi', 'includeAll', 'hide', 'allFormat', 'allValue']:
            if key in source:
                target[key] = source[key]


class EnumeratedTemplateBase(TemplatesItemBase):

    def __init__(self, data, registry, template_type, refresh):
        super(EnumeratedTemplateBase, self).__init__(data, registry)
        self._template_type = template_type
        self._refresh = refresh

    def gen_json_from_data(self, data, context):
        template_json = super(EnumeratedTemplateBase, self).gen_json_from_data(data, context)
        template_json.update({
            'type': self._template_type,
            'refresh_on_load': False,
            'datasource': None,
            'name': data['name'],
            'query': ','.join([str(options) for options in data['options']]),
            'refresh': self._refresh
        })
        if 'current' in data:
            current = data['current']
            template_json['current'] = {
                'text': current,
                'value': current
            }
        if 'options' in data:
            template_json['options'] = [{'text': option, 'value': option} for option in
                                        (data['options'])]
        return template_json


class CustomTemplate(EnumeratedTemplateBase):
    def __init__(self, data, registry):
        super(CustomTemplate, self).__init__(data, registry, 'custom', 0)


class IntervalTemplate(EnumeratedTemplateBase):
    def __init__(self, data, registry):
        super(IntervalTemplate, self).__init__(data, registry, 'interval', 2)

    def gen_json_from_data(self, data, context):
        template_json = super(IntervalTemplate, self).gen_json_from_data(data, context)
        if 'auto' in data:
            template_json['auto'] = True
            template_json['auto_count'] = (data['auto'] or {}).get('count', 30)
            template_json['auto_min'] = (data['auto'] or {}).get('min', '10s')

            auto_option = {'text': 'auto', 'value': '$__auto_interval'}
            template_json.setdefault('options', []).append(auto_option)

            if data.get('current') == 'auto':
                template_json['current'] = auto_option
        return template_json


class DatasourceTemplate(TemplatesItemBase):
    def gen_json_from_data(self, data, context):
        template_json = super(DatasourceTemplate, self).gen_json_from_data(data, context)
        template_json.update({
            'type': 'datasource',
            'name': data.get('name', 'datasource'),
            'query': data['query']
        })
        if 'current' in data:
            current = data['current']
            template_json['current'] = {
                'text': current,
                'value': current
            }

        return template_json
