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


class Links(JsonListGenerator):
    def __init__(self, data, registry):
        super(Links, self).__init__(data, registry, LinksItemBase)


class LinksItemBase(JsonGenerator):
    pass


class DashboardLink(LinksItemBase):
    def gen_json_from_data(self, data, context):
        link_json = {
            'type': 'dashboard',
            'name': 'Drilldown dashboard',
            'title': self.data.get('title', None),
            'dashboard': self.data.get('dashboard', None)
        }
        if 'params' in self.data:
            params = []
            for param in self.data.get('params'):
                if isinstance(param, str):
                    params.append((param, '$' + param))
                else:
                    for key, value in param.iteritems():
                        params.append((key, value))
            link_json['params'] = '&'.join(map(lambda pair: 'var-%s=%s' % (pair[0], pair[1]), params))
        return link_json


class AbsoluteLink(LinksItemBase):
    def gen_json_from_data(self, data, context):
        return {
            'type': 'absolute',
            'name': 'Drilldown dashboard',
            'title': self.data.get('title', None),
            'url': self.data.get('url', None)
        }
