# -*- coding: utf-8 -*-
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
from __future__ import unicode_literals

import json

from mock import MagicMock

from grafana_dashboards.client.elastic_search import ElasticSearchExporter

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


def test_elastic_search():
    exporter = ElasticSearchExporter(host='host', username='username', password='password')
    exporter._connection = MagicMock()

    dashboard_data = {'title': 'title', 'tags': []}
    exporter.process_dashboard('project_name', 'dashboard_name', dashboard_data)

    body = {'user': 'guest', 'group': 'guest', 'title': 'title', 'tags': [], 'dashboard': json.dumps(dashboard_data)}
    # noinspection PyProtectedMember
    exporter._connection.make_request.assert_called_once_with('/es/grafana-dash/dashboard/dashboard_name',
                                                              body)


def test_elastic_search_with_kerberos():
    exporter = ElasticSearchExporter(host='host', use_kerberos='true')
    exporter._connection = MagicMock()

    dashboard_data = {'title': 'title', 'tags': []}
    exporter.process_dashboard('project_name', 'dashboard_name', dashboard_data)

    body = {'user': 'guest', 'group': 'guest', 'title': 'title', 'tags': [], 'dashboard': json.dumps(dashboard_data)}
    # noinspection PyProtectedMember
    exporter._connection.make_request.assert_called_once_with('/es/grafana-dash/dashboard/dashboard_name',
                                                              body)
