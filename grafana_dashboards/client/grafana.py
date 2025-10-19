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

import logging
import os
from pathlib import Path
from typing import TypedDict, cast
try:
    # Try the standard library import (Python 3.11+)
    from typing import Unpack
except ImportError:
    # Fallback for older versions (Python < 3.11)
    from typing_extensions import Unpack

from grafana_dashboards.client.connection import BasicAuthConnection, BearerAuthConnection, ConnectionInterface, KerberosConnection, SSLAuthConnection
from grafana_dashboards.exporter import DashboardExporter

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


logger = logging.getLogger(__name__)


class GrafanaExporterParams(TypedDict, total=False):
    host: str
    username: str
    password: str
    token: str
    use_kerberos: bool
    ssl_client_crt: str
    ssl_client_key: str
    commit_message: str


class GrafanaExporter(DashboardExporter):
    _connection: ConnectionInterface

    def __init__(self, **kwargs: Unpack[GrafanaExporterParams]):
        super().__init__()
        self._commit_message = kwargs.get('commit_message', "")
        self._host = cast(str, os.getenv('GRAFANA_HOST', kwargs.get('host')))
        password = cast(str, os.getenv('GRAFANA_PASSWORD', kwargs.get('password')))
        username = cast(str, os.getenv('GRAFANA_USERNAME', kwargs.get('username')))
        auth_token = cast(str, os.getenv('GRAFANA_TOKEN', kwargs.get('token')))
        use_kerberos = os.getenv('GRAFANA_USE_KERBEROS', kwargs.get('use_kerberos'))
        client_crt = cast(str, os.getenv('GRAFANA_SSL_CLIENT_CRT', kwargs.get('ssl_client_crt')))

        if use_kerberos:
            self._connection = KerberosConnection(self._host)
        elif auth_token:
            self._connection = BearerAuthConnection(auth_token, self._host)
        elif client_crt:
            client_key = cast(str, os.getenv('GRAFANA_SSL_CLIENT_KEY', kwargs.get('ssl_client_key')))
            derived_key_path = Path(f'{Path(client_crt).stem}.key')
            cert_bundle: tuple[str, str] | str
            # pull the separate key also if not given explicitly and derived filename exists
            if client_key or (not client_key and derived_key_path.exists()):
                cert_bundle = (client_crt, client_key if client_key else str(derived_key_path))
            # otherwise assume bundled PEM
            else:
                cert_bundle = client_crt
            self._connection = SSLAuthConnection(self._host, cert_bundle)
        else:
            self._connection = BasicAuthConnection(username, password, self._host)

    def process_dashboard(self, project_name: str, dashboard_name: str, dashboard_data: dict[str, str]) -> None:
        super().process_dashboard(project_name, dashboard_name, dashboard_data)

        body = {'overwrite': True, 'dashboard': dashboard_data, 'message': self._commit_message}

        if 'folderId' in dashboard_data:
            body.update({'folderId': dashboard_data['folderId']})

        if 'uid' in dashboard_data:
            body.update({'uid': dashboard_data['uid']})

        logger.info("Uploading dashboard '%s' to %s", dashboard_name, self._host)
        self._connection.make_request('/api/dashboards/db', body)
