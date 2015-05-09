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
        processed_parts = []
        queries = []
        if not self.data.get('query'):
            return queries
        for query_part in self.data['query'].split('.'):
            if query_part.startswith('$'):
                is_first = False if queries else True
                template_json = {
                    'type': 'query',
                    'refresh_on_load': is_first,
                    'name': query_part[1:],
                    'query': '.'.join(processed_parts + ['*']),
                    'refresh': is_first
                }
                queries.append(template_json)
            processed_parts.append(query_part)
        return queries
