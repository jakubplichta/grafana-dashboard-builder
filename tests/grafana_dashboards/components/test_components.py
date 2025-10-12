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
import inspect
import json
from pathlib import Path

import mock as mock
import yaml

import grafana_dashboards.common
from grafana_dashboards.components import *  # NOQA
from grafana_dashboards.components.base import JsonListGenerator
from grafana_dashboards.errors import UnregisteredComponentError

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


def pytest_generate_tests(metafunc):
    fixtures = []
    ids = []
    for (component, test, config, output) in load_test_fixtures():
        fixtures.append((component, config, output))
        ids.append(f'{grafana_dashboards.common.get_component_type(component)};{test}')
    metafunc.parametrize('component,config,expected', fixtures, ids=ids)


def load_test_fixtures():
    for component in base.get_generators():  # NOQA
        component_type = grafana_dashboards.common.get_component_type(component)
        dirname = Path(__file__).resolve().parent / component_type
        if not dirname.is_dir():
            continue
        for f in dirname.iterdir():
            if f.suffix != '.yaml':
                continue
            filename = f.stem
            with open(dirname / f'{filename}.yaml', 'r') as fp:
                config = yaml.load(fp, Loader=yaml.FullLoader)
            with open(dirname / f'{filename}.json', 'r') as fp:
                output = json.load(fp)
            yield component, filename, config, output


def test_component(component, config, expected):
    with mock.patch('grafana_dashboards.components.base.ComponentRegistry') as registry:
        def create_component(component_type, data):
            gen = mock.Mock()
            if inspect.isclass(component_type) and issubclass(component_type, JsonListGenerator):
                gen.gen_json = mock.Mock(return_value=['mocked ' + str(component_type)])
            else:
                gen.gen_json = mock.Mock(return_value='mocked ' + str(component_type))
            return gen

        registry.create_component = mock.Mock(side_effect=create_component)

        def get_component(component_type, name):
            if name == 'not-mocked':
                raise UnregisteredComponentError(f"No component '{component_type}' with name '{name}' found!")

            gen = mock.Mock()
            gen.gen_json = mock.Mock(return_value=[f'mocked {str(component_type)} for name {name}'])
            return gen

        registry.get_component = mock.Mock(side_effect=get_component)
        assert component(config, registry).gen_json() == expected
