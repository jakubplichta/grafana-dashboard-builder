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
import logging
import os

from grafana_dashboards.client.connection import Connection, KerberosConnection
from grafana_dashboards.exporter import DashboardExporter

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


logger = logging.getLogger(__name__)


class GrafanaExporter(DashboardExporter):
    def __init__(self, **kwargs):
        super(GrafanaExporter, self).__init__()
        self._host = os.getenv('GRAFANA_HOST', kwargs.get('host'))
        password = os.getenv('GRAFANA_PASSWORD', kwargs.get('password'))
        username = os.getenv('GRAFANA_USERNAME', kwargs.get('username'))
        use_kerberos = os.getenv('GRAFANA_USE_KERBEROS', kwargs.get('use_kerberos'))

        if use_kerberos:
            self._connection = KerberosConnection(self._host)
        else:
            self._connection = Connection(username, password, self._host)

    def process_dashboard(self, project_name, dashboard_name, dashboard_data):
        super(GrafanaExporter, self).process_dashboard(project_name, dashboard_name, dashboard_data)
        body = {'overwrite': True, 'dashboard': dashboard_data}
        logger.info("Uploading dashboard '%s' to %s", dashboard_name, self._host)
        self._connection.make_request('/api/dashboards/db', body)
