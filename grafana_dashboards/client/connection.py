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
import base64
import json
import logging
from http.cookiejar import CookieJar
from urllib.parse import urlparse
from urllib.request import build_opener, HTTPHandler, HTTPSHandler, HTTPCookieProcessor, HTTPDefaultErrorHandler, \
    Request, BaseHandler

import requests
from requests_kerberos import HTTPKerberosAuth

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'

logger = logging.getLogger(__name__)


class BaseConnection(object):
    _headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(self, host, auth_header, debug=0):
        self._host = host
        self._headers['Authorization'] = auth_header

        self._opener = build_opener(HTTPHandler(debuglevel=debug),
                                    HTTPSHandler(debuglevel=debug),
                                    HTTPCookieProcessor(CookieJar()),
                                    LoggingHandler(),
                                    HTTPDefaultErrorHandler())

    def make_request(self, uri, body=None):
        request = Request(f'{self._host}{uri}',
                          json.dumps(body).encode('utf-8') if body else None,
                          headers=self._headers)
        response_body = self._opener.open(request).read()
        return {} if (response_body is None or response_body == '') else json.loads(response_body)


class BasicAuthConnection(BaseConnection):
    def __init__(self, username, password, host, debug=0):
        logger.debug('Creating new connection with username=%s host=%s', username, host)

        base64string = base64.encodebytes(f'{username}:{password}'.encode('utf-8')).replace(b'\n', b'')

        super().__init__(host, b'Basic ' + base64string, debug)


class BearerAuthConnection(BaseConnection):
    def __init__(self, token, host, debug=0):
        logger.debug('Creating new connection with token=%s host=%s', token[:5], host)

        super().__init__(host, f'Bearer {token.strip()}', debug)


class LoggingHandler(BaseHandler):
    def __init__(self):
        pass

    # noinspection PyMethodMayBeStatic
    def http_request(self, request):
        path = urlparse(request.get_full_url()).path
        logger.debug('Sending request: method=%s uri=%s', request.get_method(), path)
        return request

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def http_response(self, request, response):
        logger.debug('Response received: status=%s msg=%s', response.getcode(), response.msg)
        return response

    https_request = http_request
    https_response = http_response


class KerberosConnection(object):
    def __init__(self, host):
        logger.debug('Creating new kerberos connection with host=%s', host)
        self._host = host

    def make_request(self, uri, body=None):
        response = requests.post(f'{self._host}{uri}', json=body, auth=HTTPKerberosAuth(), verify=False)
        return response.json()


class SSLAuthConnection(object):
    def __init__(self, host, cert_bundle, debug=0):
        logger.debug('Using SSL client cert from "%s" with host=%s', cert_bundle, host)
        self._host = host
        self._cert = cert_bundle

    def make_request(self, uri, body=None):
        response = requests.post(f'{self._host}{uri}', json=body, cert=self._cert)
        return response.json()
