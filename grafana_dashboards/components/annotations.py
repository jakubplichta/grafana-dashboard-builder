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


class Annotations(JsonListGenerator):
    def __init__(self, data, registry):
        super(Annotations, self).__init__(data, registry, AnnotationsItemBase)


class AnnotationsItemBase(JsonGenerator):
    pass


class Annotation(AnnotationsItemBase):
    _copy_fields = {'datasource'}

    def gen_json_from_data(self, data, context):
        template_json = super(Annotation, self).gen_json_from_data(data, context)
        template_json['name'] = data['name']
        template_json['expr'] = data['expr']
        template_json['enable'] = data.get('enable', True)
        template_json['hide'] = data.get('hide', False)
        template_json['iconColor'] = data.get('iconColor', 'rgba(255, 96, 96, 1)')
        template_json['showIn'] = data.get('showIn', 0)
        return template_json
