# -*- coding: utf-8 -*-
# Copyright 2015-2019 grafana-dashboard-builder contributors
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

import logging
import os

from grafana_dashboards.client.connection import (KerberosConnection,
                                                  BearerAuthConnection,
                                                  BasicAuthConnection,
                                                  SSLAuthConnection)
from grafana_dashboards.exporter import DashboardExporter

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


logger = logging.getLogger(__name__)


class GrafanaExporter(DashboardExporter):
    def __init__(self, **kwargs):
        super(GrafanaExporter, self).__init__()
        self._host = os.getenv('GRAFANA_HOST', kwargs.get('host'))
        password = os.getenv('GRAFANA_PASSWORD', kwargs.get('password'))
        username = os.getenv('GRAFANA_USERNAME', kwargs.get('username'))
        auth_token = os.getenv('GRAFANA_TOKEN', kwargs.get('token'))
        use_kerberos = os.getenv('GRAFANA_USE_KERBEROS', kwargs.get('use_kerberos'))
        client_crt = os.getenv('GRAFANA_SSL_CLIENT_CRT', kwargs.get('ssl_client_crt'))

        if use_kerberos:
            self._connection = KerberosConnection(self._host)
        elif auth_token:
            self._connection = BearerAuthConnection(auth_token, self._host)
        elif client_crt:
            client_key = os.getenv('GRAFANA_SSL_CLIENT_KEY', kwargs.get('ssl_client_key'))
            derived_key_path = os.path.splitext(client_crt)[0] + '.key'
            # pull the separate key also if not given explicitly and derived filename exists
            if client_key or (not client_key and os.path.exists(derived_key_path)):
                cert_bundle = (client_crt, client_key if client_key else derived_key_path)
            # otherwise assume bundled PEM
            else:
                cert_bundle = client_crt
            self._connection = SSLAuthConnection(self._host, cert_bundle)
        else:
            self._connection = BasicAuthConnection(username, password, self._host)

    def process_dashboard(self, project_name, dashboard_name, dashboard_data):
        super(GrafanaExporter, self).process_dashboard(project_name, dashboard_name, dashboard_data)
        body = {'overwrite': True, 'dashboard': dashboard_data}

        if 'folderId' in dashboard_data:
            body.update({'folderId': dashboard_data['folderId']})

        logger.info("Uploading dashboard '%s' to %s", dashboard_name, self._host)
        self._connection.make_request('/api/dashboards/db', body)
