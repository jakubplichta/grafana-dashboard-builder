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

from unittest.mock import MagicMock

from grafana_dashboards.client.grafana import GrafanaExporter

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


def test_grafana():
    exporter = GrafanaExporter(host='host', username='username', password='password')
    exporter._connection = MagicMock()

    dashboard_data = {'title': 'title', 'tags': []}
    exporter.process_dashboard('project_name', 'dashboard_name', dashboard_data)

    body = {'overwrite': True, 'dashboard': dashboard_data, 'message': ''}
    # noinspection PyProtectedMember
    exporter._connection.make_request.assert_called_once_with('/api/dashboards/db',
                                                              body)


def test_grafana_with_kerberos():
    exporter = GrafanaExporter(host='host', use_kerberos='true')
    exporter._connection = MagicMock()

    dashboard_data = {'title': 'title', 'tags': []}
    exporter.process_dashboard('project_name', 'dashboard_name', dashboard_data)

    body = {'overwrite': True, 'dashboard': dashboard_data, 'message': ''}
    # noinspection PyProtectedMember
    exporter._connection.make_request.assert_called_once_with('/api/dashboards/db',
                                                              body)


def test_grafana_with_sslauth():
    exporter = GrafanaExporter(host='host', ssl_client_crt='/file/fake')
    exporter._connection = MagicMock()

    dashboard_data = {'title': 'title', 'tags': []}
    exporter.process_dashboard('project_name', 'dashboard_name', dashboard_data)

    body = {'overwrite': True, 'dashboard': dashboard_data, 'message': ''}
    # noinspection PyProtectedMember
    exporter._connection.make_request.assert_called_once_with('/api/dashboards/db',
                                                              body)
