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


class Yaxes(JsonListGenerator):
    def __init__(self, data, registry):
        super(Yaxes, self).__init__(data, registry, YaxesItemBase)

    def gen_json_from_data(self, data, context):
        if len(data) == 1:
            data.append(data[0])
        return super(Yaxes, self).gen_json_from_data(data, context)

    def gen_item_json(self, items, result_list):
        if isinstance(items, dict) and len(items) > 1:
            result_list.append(items)
        else:
            super(Yaxes, self).gen_item_json(items, result_list)


class YaxesItemBase(JsonGenerator):
    pass


class Yaxis(YaxesItemBase):
    def gen_json_from_data(self, data, context):
        yaxis_json = super(Yaxis, self).gen_json_from_data(data, context)
        yaxis_json.update({
            'format': data.get('format', 'short'),
            'label': data.get('label', None),
            'logBase': data.get('logBase', 1),
            'max': data.get('max', None),
            'min': data.get('min', None),
            'show': data.get('show', True)
        })
        return yaxis_json
