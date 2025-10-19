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

import json
import logging
import os
from typing import TypedDict, cast
try:
    # Try the standard library import (Python 3.11+)
    from typing import Unpack
except ImportError:
    # Fallback for older versions (Python < 3.11)
    from typing_extensions import Unpack

from grafana_dashboards.client.connection import BasicAuthConnection, ConnectionInterface, KerberosConnection
from grafana_dashboards.exporter import DashboardExporter

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


logger = logging.getLogger(__name__)


class ElasticSearchExporterParams(TypedDict, total=False):
    host: str
    username: str
    password: str
    use_kerberos: bool | str


class ElasticSearchExporter(DashboardExporter):
    _connection: ConnectionInterface

    def __init__(self, **kwargs: Unpack[ElasticSearchExporterParams]) -> None:
        super().__init__()
        self._host = cast(str, os.getenv('ES_HOST', kwargs.get('host')))
        password = cast(str, os.getenv('ES_PASSWORD', kwargs.get('password')))
        username = cast(str, os.getenv('ES_USERNAME', kwargs.get('username')))
        use_kerberos = os.getenv('ES_USE_KERBEROS', kwargs.get('use_kerberos'))

        if use_kerberos:
            self._connection = KerberosConnection(self._host)
        else:
            self._connection = BasicAuthConnection(username, password, self._host)

    def process_dashboard(self, project_name: str, dashboard_name: str, dashboard_data: dict[str, str]) -> None:
        super().process_dashboard(project_name, dashboard_name, dashboard_data)
        body = {'user': 'guest', 'group': 'guest', 'title': dashboard_data['title'], 'tags': dashboard_data['tags'],
                'dashboard': json.dumps(dashboard_data)}
        logger.info("Uploading dashboard '%s' to %s", dashboard_name, self._host)
        self._connection.make_request(f'/es/grafana-dash/dashboard/{dashboard_name}', body)
