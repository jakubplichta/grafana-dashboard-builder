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
from pathlib import Path
from unittest.mock import patch

from grafana_dashboards import cli
from grafana_dashboards.config import Config

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class DummyExporter:

    def __init__(self, prop, **kwargs):
        super().__init__()
        self.prop = prop
        self.kwargs = kwargs


def test_initialize_exporters():
    config_file = Path(__file__).resolve().parent / 'config.yaml'
    config = Config(config_file)
    # noinspection PyProtectedMember
    exporters = cli._initialize_exporters('dummy', [DummyExporter], config)

    assert exporters is not None
    assert len(exporters) == 1
    assert exporters[0].prop == 'value'
    assert exporters[0].kwargs == {'other': True}


# noinspection PyUnusedLocal
@patch('os.walk', return_value=[('/path', ['dir1', 'dir2'], ['file1', 'file2'])])
@patch('pathlib.Path.is_dir', return_value=True)
def test_process_paths(isdir, walk):
    # noinspection PyProtectedMember
    paths = cli._process_paths(['/path'])

    # noinspection PySetFunctionToLiteral
    assert paths == {'/path/file1', '/path/file2'}
