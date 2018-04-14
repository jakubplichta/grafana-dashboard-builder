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
from grafana_dashboards.components.base import ComponentBase, get_placeholders
from grafana_dashboards.components.dashboards import Dashboard
from grafana_dashboards.context import Context

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class Project(ComponentBase):
    def __init__(self, data, registry):
        super(Project, self).__init__(data, registry)
        self._placeholders = [placeholder for dashboard in self._get_dashboard_names()
                              for placeholder in get_placeholders(dashboard)]

    def _get_dashboard_names(self):
        return self.data.get('dashboards', [])

    def get_dashboards(self):
        return [self.registry.get_component(Dashboard, dashboard_name) for dashboard_name in
                self._get_dashboard_names()]

    def get_contexts(self, context=None):
        if context is None:
            context = {}
        data = self.data.copy()
        data.update(context)
        return Context.create_context(data, self._placeholders)
