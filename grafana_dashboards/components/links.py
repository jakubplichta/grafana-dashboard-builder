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


class Links(JsonListGenerator):
    def __init__(self, data, registry):
        super(Links, self).__init__(data, registry, LinksItemBase)


class LinksItemBase(JsonGenerator):
    pass


class DashboardLink(LinksItemBase):
    def gen_json_from_data(self, data, context):
        link_json = super(DashboardLink, self).gen_json_from_data(data, context)
        link_json.update({
            'type': 'dashboard',
            'name': 'Drilldown dashboard',
            'title': data.get('title', None),
            'dashboard': data.get('dashboard', None)
        })
        if 'params' in data and isinstance(data.get('params'), list):
            params = []
            for param in data.get('params'):
                if isinstance(param, str):
                    params.append((param, '$' + param))
                else:
                    for key, value in param.iteritems():
                        params.append((key, value))
            link_json['params'] = '&'.join(map(lambda pair: 'var-%s=%s' % (pair[0], pair[1]), params))
        return link_json


class AbsoluteLink(LinksItemBase):
    def gen_json_from_data(self, data, context):
        link_json = super(AbsoluteLink, self).gen_json_from_data(data, context)
        link_json.update({
            'type': 'absolute',
            'name': 'Drilldown dashboard',
            'title': data.get('title', None),
            'url': data.get('url', None)
        })
        return link_json
