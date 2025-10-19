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
from __future__ import annotations

from typing import Any

from grafana_dashboards.components.base import ComponentRegistry, JsonListGenerator, ObjectJsonGenerator

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'

from grafana_dashboards.context import Context


class Yaxes(JsonListGenerator):
    def __init__(self, data: dict[str, Any], registry: ComponentRegistry) -> None:
        super().__init__(data, registry, [YaxesItemBase])

    def gen_json_from_data(self, data: list[Any], context: Context) -> list[Any]:
        if len(data) == 1:
            data.append(data[0])
        return super().gen_json_from_data(data, context)

    def gen_item_json(self, items: str | dict[str, Any], result_list: list[Any]) -> None:
        if isinstance(items, dict) and len(items) > 1:
            result_list.append(items)
        else:
            super().gen_item_json(items, result_list)


class YaxesItemBase(ObjectJsonGenerator):
    pass


class Yaxis(YaxesItemBase):
    def gen_json_from_data(self, data: dict[str, Any], context: Context) -> dict[str, Any]:
        yaxis_json = super().gen_json_from_data(data, context)
        yaxis_json.update({
            'format': data.get('format', 'short'),
            'label': data.get('label', None),
            'logBase': data.get('logBase', 1),
            'max': data.get('max', None),
            'min': data.get('min', None),
            'show': data.get('show', True)
        })
        return yaxis_json
