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
import urllib2

from mock import MagicMock, patch
from requests_kerberos import HTTPKerberosAuth

from grafana_dashboards.client.connection import Connection, KerberosConnection

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class Capture(object):
    """
    Class for use in method call verification that captures call argument that can be tested later on.
    """
    def __eq__(self, other):
        """
        Captures argument and always returns true to make verification successful.
        :return: True
        """
        self.value = other
        return True


def test_connection():
    connection = Connection('username', 'password', 'https://host')
    connection._opener = MagicMock()
    # noinspection PyProtectedMember
    connection._opener.open().read.return_value = '{"hello":"world"}'

    assert connection.make_request('/uri', {'it\'s': 'alive'}) == {'hello': 'world'}

    request = urllib2.Request('https://host/uri',
                              '{"it\'s": "alive"}',
                              headers={
                                  'Content-type': 'application/json',
                                  'Accept': 'application/json',
                                  'Authorization': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='
                              })
    capture = Capture()
    # noinspection PyProtectedMember
    connection._opener.open.assert_called_with(capture)
    assert request.get_full_url() == capture.value.get_full_url()
    assert request.header_items() == capture.value.header_items()
    assert request.get_method() == capture.value.get_method()
    assert request.get_data() == capture.value.get_data()


@patch('requests.post')
def test_connection_with_kerberos(post):
    connection = KerberosConnection('https://host')

    post().json.return_value = {'hello': 'world'}

    assert connection.make_request('/uri', {'it\'s': 'alive'}) == {'hello': 'world'}

    capture = Capture()
    post.assert_called_with('https://host/uri', auth=capture, json={"it's": 'alive'}, verify=False)
    assert isinstance(capture.value, HTTPKerberosAuth)
