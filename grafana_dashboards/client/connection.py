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

import abc
import base64
import json
import logging
from http.cookiejar import CookieJar
from typing import Any
from urllib.parse import urlparse
from urllib.request import BaseHandler, HTTPCookieProcessor, HTTPDefaultErrorHandler, HTTPHandler, HTTPSHandler, Request, build_opener

import requests
from requests_kerberos import HTTPKerberosAuth

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'

logger = logging.getLogger(__name__)


class ConnectionInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return (hasattr(subclass, 'make_request') and
                callable(subclass.make_request) or
                NotImplemented)

    @abc.abstractmethod
    def make_request(self, uri: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        raise NotImplementedError


class BaseConnection(ConnectionInterface):
    _headers: dict[str, str] = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(self, host: str, auth_header: str, debug: int = 0) -> None:
        self._host = host
        self._headers['Authorization'] = auth_header

        self._opener = build_opener(HTTPHandler(debuglevel=debug),
                                    HTTPSHandler(debuglevel=debug),
                                    HTTPCookieProcessor(CookieJar()),
                                    LoggingHandler(),
                                    HTTPDefaultErrorHandler())

    def make_request(self, uri: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        request = Request(f'{self._host}{uri}',
                          json.dumps(body).encode('utf-8') if body else None,
                          headers=self._headers)
        response_body = self._opener.open(request).read()
        return {} if (response_body is None or response_body == '') else json.loads(response_body)


class BasicAuthConnection(BaseConnection):
    def __init__(self, username: str, password: str, host: str, debug: int = 0) -> None:
        logger.debug('Creating new connection with username=%s host=%s', username, host)

        base64string = base64.encodebytes(f'{username}:{password}'.encode()).replace(b'\n', b'').decode('utf-8')

        super().__init__(host, f'Basic {base64string}', debug)


class BearerAuthConnection(BaseConnection):
    def __init__(self, token: str, host: str, debug: int = 0) -> None:
        logger.debug('Creating new connection with token=%s host=%s', token[:5], host)

        super().__init__(host, f'Bearer {token.strip()}', debug)


class LoggingHandler(BaseHandler):
    def __init__(self) -> None:
        pass

    # noinspection PyMethodMayBeStatic
    def http_request(self, request: Request) -> Request:
        path = urlparse(request.get_full_url()).path
        logger.debug('Sending request: method=%s uri=%s', request.get_method(), path)
        return request

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def http_response(self, request: Request, response):  # type: ignore
        logger.debug('Response received: status=%s msg=%s', response.getcode(), response.msg)
        return response

    https_request = http_request
    https_response = http_response


class KerberosConnection(ConnectionInterface):
    def __init__(self, host: str) -> None:
        logger.debug('Creating new kerberos connection with host=%s', host)
        self._host = host

    def make_request(self, uri: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        response = requests.post(f'{self._host}{uri}', json=body, auth=HTTPKerberosAuth(), verify=False)
        return response.json()


class SSLAuthConnection(ConnectionInterface):
    def __init__(self, host: str, cert_bundle: str | tuple[str, str] | None, debug: int = 0):
        logger.debug('Using SSL client cert from "%s" with host=%s', cert_bundle, host)
        self._host = host
        self._cert = cert_bundle

    def make_request(self, uri: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        response = requests.post(f'{self._host}{uri}', json=body, cert=self._cert)
        return response.json()
