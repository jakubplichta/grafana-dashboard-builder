# -*- coding: utf-8 -*-
# Copyright 2015-2016 grafana-dashboard-builder contributors
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
import json
import os

import mock as mock
import yaml

import grafana_dashboards.common
from grafana_dashboards.components import *  # NOQA

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


def pytest_generate_tests(metafunc):
    fixtures = []
    ids = []
    for (component, test, config, output) in load_test_fixtures():
        fixtures.append((component, config, output))
        ids.append('%s;%s' % (grafana_dashboards.common.get_component_type(component), test))
    metafunc.parametrize('component,config,expected', fixtures, ids=ids)


def load_test_fixtures():
    for component in base.get_generators():  # NOQA
        component_type = grafana_dashboards.common.get_component_type(component)
        dirname = os.path.join(os.path.dirname(os.path.abspath(__file__)), component_type)
        if not os.path.isdir(dirname):
            continue
        for f in os.listdir(dirname):
            if not f.endswith('.yaml'):
                continue
            filename = f[:-5]
            with file(os.path.join(dirname, '%s.yaml' % filename), 'r') as fp:
                config = yaml.load(fp)
            with file(os.path.join(dirname, '%s.json' % filename), 'r') as fp:
                output = json.load(fp)
            yield component, filename, config, output


def test_component(component, config, expected):
    with mock.patch('grafana_dashboards.components.base.ComponentRegistry') as registry:
        gen = mock.Mock()
        gen.gen_json = mock.Mock(return_value=['mocked'])
        registry.create_component = mock.Mock(return_value=gen)
        gen = mock.Mock()
        gen.gen_json = mock.Mock(return_value=['mocked1', 'mocked2'])
        registry.get_component = mock.Mock(return_value=gen)
        assert component(config, registry).gen_json() == expected
