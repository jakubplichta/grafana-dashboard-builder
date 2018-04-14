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
from grafana_dashboards.common import get_component_type
from grafana_dashboards.components.panels import Panels

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class Rows(JsonListGenerator):
    def __init__(self, data, registry):
        super(Rows, self).__init__(data, registry, RowsItemBase)


class RowsItemBase(JsonGenerator):
    pass


class Row(RowsItemBase):

    _copy_fields = {'repeat'}

    def gen_json_from_data(self, data, context):
        row_json = super(Row, self).gen_json_from_data(data, context)
        row_json.update({
            'title': data.get('title', ''),
            'height': data.get('height', '250px'),
            'showTitle': data.get('showTitle', False),
            'collapse': data.get('collapse', False),
            'panels': []
        })
        if get_component_type(Panels) in data:
            row_json['panels'] = self.registry.create_component(Panels, data).gen_json()
        return row_json
