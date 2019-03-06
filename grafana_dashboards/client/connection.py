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

import base64
import json
import logging

try:
    from cookielib import CookieJar
except ImportError:
    from http.cookiejar import CookieJar
try:
    from urllib2 import build_opener, HTTPHandler, HTTPSHandler, HTTPCookieProcessor, HTTPDefaultErrorHandler, \
        Request, BaseHandler
except ImportError:
    from urllib.request import build_opener, HTTPHandler, HTTPSHandler, HTTPCookieProcessor, HTTPDefaultErrorHandler, \
        Request, BaseHandler
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

import requests
from requests_kerberos import HTTPKerberosAuth

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'

logger = logging.getLogger(__name__)


class Connection(object):
    _headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(self, username, password, host, debug=0):
        logger.debug('Creating new connection with username=%s host=%s', username, host)
        self._host = host

        base64string = base64.encodestring(('%s:%s' % (username, password)).encode('utf-8')).replace(b'\n', b'')
        self._headers['Authorization'] = b'Basic ' + base64string

        self._opener = build_opener(HTTPHandler(debuglevel=debug),
                                    HTTPSHandler(debuglevel=debug),
                                    HTTPCookieProcessor(CookieJar()),
                                    LoggingHandler(),
                                    HTTPDefaultErrorHandler())

    def make_request(self, uri, body=None):
        request = Request('{0}{1}'.format(self._host, uri),
                          json.dumps(body).encode('utf-8') if body else None,
                          headers=self._headers)
        response_body = self._opener.open(request).read()
        return {} if (response_body is None or response_body == '') else json.loads(response_body)


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
        response = requests.post('{0}{1}'.format(self._host, uri), json=body, auth=HTTPKerberosAuth(), verify=False)
        return response.json()
