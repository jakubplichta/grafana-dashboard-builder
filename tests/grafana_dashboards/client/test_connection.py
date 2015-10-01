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
import urllib2

from mock import MagicMock

from grafana_dashboards.client.connection import Connection

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


def test_elastic_search():
    connection = Connection('username', 'password', 'https://host')
    connection._opener = MagicMock()
    # noinspection PyProtectedMember
    connection._opener.open().read.return_value = '{"hello":"world"}'

    assert connection.make_request('/uri', {'it\'s': 'alive'}) == {'hello': 'world'}

    request = urllib2.Request('https://host/uri',
                              '{"it\'s":"alive"}',
                              headers={
                                  'Content-type': 'application/json',
                                  'Accept': 'application/json',
                                  'Authorization': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='
                              })
    # noinspection PyProtectedMember,PyUnresolvedReferences
    connection._opener.open.verify_called_once_with(request)
