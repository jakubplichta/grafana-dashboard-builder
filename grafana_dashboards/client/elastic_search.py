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
import json
import os

from grafana_dashboards.exporter import DashboardExporter
from grafana_dashboards.client.connection import Connection

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class ElasticSearchExporter(DashboardExporter):
    def __init__(self, **kwargs):
        super(ElasticSearchExporter, self).__init__()
        host = os.getenv('ES_HOST', kwargs.get('host'))
        password = os.getenv('ES_PASSWORD', kwargs.get('password'))
        username = os.getenv('ES_USERNAME', kwargs.get('username'))

        self._connection = Connection(username, password, host)

    def process_dashboard(self, project_name, dashboard_name, dashboard_data):
        super(ElasticSearchExporter, self).process_dashboard(project_name, dashboard_name, dashboard_data)
        body = {'user': 'guest', 'group': 'guest', 'title': dashboard_data['title'], 'tags': dashboard_data['tags'],
                'dashboard': json.dumps(dashboard_data)}
        self._connection.make_request('/es/grafana-dash/dashboard/{0}'.format(dashboard_name), body)
