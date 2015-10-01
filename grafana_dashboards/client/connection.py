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
import base64
import cookielib
import json
import logging
import urllib2
from urlparse import urlparse

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

        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        self._headers['Authorization'] = 'Basic %s' % base64string

        self._opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=debug),
                                            urllib2.HTTPSHandler(debuglevel=debug),
                                            urllib2.HTTPCookieProcessor(cookielib.CookieJar()),
                                            LoggingHandler(),
                                            urllib2.HTTPDefaultErrorHandler())

    def make_request(self, uri, body=None):
        request = urllib2.Request('{0}{1}'.format(self._host, uri),
                                  json.dumps(body) if body else None,
                                  headers=self._headers)
        response_body = self._opener.open(request).read()
        return {} if (response_body is None or response_body == '') else json.loads(response_body)


class LoggingHandler(urllib2.BaseHandler):
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
