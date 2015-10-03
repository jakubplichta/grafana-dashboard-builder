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
        for query_part in data['query'].split('.'):
            if query_part.startswith('$'):
                is_first = False if queries else True
                query = query_part[1:]
                metric = '*'
                template_json = {
                    'type': 'query',
                    'refresh_on_load': is_first,
                    'name': query,
                    'refresh': is_first
                }
                if query in data:
                    query_config = data[query]
                    metric = query_config.get('metric', metric)
                    if 'current' in query_config:
                        current = query_config['current']
                        template_json['current'] = {
                            'text': current,
                            'value': current
                        }
                    if 'options' in query_config:
                        template_json['options'] = [{'text': option, 'value': option} for option in
                                                    (query_config['options'])]
                template_json['query'] = '.'.join(processed_parts + [metric])
                queries.append(template_json)
            processed_parts.append(query_part)
        return queries


class CustomTemplate(TemplatesItemBase):
    def gen_json_from_data(self, data, context):
        template_json = super(CustomTemplate, self).gen_json_from_data(data, context)
        template_json.update({
            'type': 'custom',
            'refresh_on_load': False,
            'name': data['name'],
            'query': ','.join(data['options'])
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
        return [template_json]
