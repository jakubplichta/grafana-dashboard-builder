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
from unittest.mock import MagicMock, patch

import pytest

from grafana_dashboards.exporter import FileExporter, ProjectProcessor

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


def test_project_processor():
    dashboard_processor = MagicMock()
    processor = ProjectProcessor([dashboard_processor])
    project = MagicMock()
    context = MagicMock()
    dashboard = MagicMock()
    project.get_contexts.return_value = [context]
    project.get_dashboards.return_value = [dashboard]
    parent_context = MagicMock()

    # noinspection PyTypeChecker
    processor.process_projects([project], parent_context)

    project.get_contexts.assert_called_once_with(parent_context)
    dashboard.gen_json.assert_called_with(context)
    context.expand_placeholders.assert_called_with(dashboard.name)
    dashboard_processor.process_dashboard.assert_called_once_with(project.name, context.expand_placeholders(),
                                                                  dashboard.gen_json())


@patch('grafana_dashboards.exporter.open', create=True)
@patch('json.dump')
@patch('pathlib.Path.mkdir', return_value=True)
@patch('pathlib.Path.is_dir', return_value=True)
@patch('pathlib.Path.exists', return_value=True)
def test_file_exporter(patch_exists, path_isdir, makedirs, json_dump, mock_file):
    exporter = FileExporter('output_folder')

    dashboard_data = {'some_key': 'some_value'}
    exporter.process_dashboard('project_name', 'dashboard_name', dashboard_data)

    json_dump.assert_called_once_with(dashboard_data, mock_file().__enter__(), sort_keys=True, indent=2,
                                      separators=(',', ': '))


@patch('pathlib.Path.mkdir', side_effect=[True, OSError('testing')])
@patch('pathlib.Path.is_dir', return_value=True)
@patch('pathlib.Path.exists', return_value=False)
def test_file_exporter_path_not_exist(patch_exists, path_isdir, makedirs):
    exporter = FileExporter('output_folder')

    dashboard_data = {'some_key': 'some_value'}
    with pytest.raises(Exception) as e:
        exporter.process_dashboard('project_name', 'dashboard_name', dashboard_data)
    assert 'testing' in str(e.value)


@patch('pathlib.Path.mkdir', return_value=True)
@patch('pathlib.Path.is_dir', return_value=False)
@patch('pathlib.Path.exists', return_value=False)
def test_file_exporter_output_not_dir(patch_exists, path_isdir, makedirs):
    with pytest.raises(Exception) as e:
        FileExporter('output_folder')

    assert "'output_folder' must be a directory" in str(e.value)
