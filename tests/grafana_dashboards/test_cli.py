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

from mock import patch

from grafana_dashboards import cli

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


# noinspection PyUnusedLocal
@patch('os.walk', return_value=[('/path', ['dir1', 'dir2'], ['file1', 'file2'])])
@patch('os.path.isdir', return_value=True)
def test_process_paths(isdir, walk):
    # noinspection PyProtectedMember
    paths = cli._process_paths(['/path'])

    # noinspection PySetFunctionToLiteral
    assert paths == set(['/path/file1', '/path/file2'])
