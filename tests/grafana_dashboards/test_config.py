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
import os

from grafana_dashboards.config import Config

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


def test_existent_config_file():
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')
    config = Config(config_file)

    assert config.get_config('context') == {'component': 'frontend'}
    assert config.get_config('unknown') == {}


def test_nonexistent_config_file():
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'no_file.yaml')
    config = Config(config_file)

    assert config.get_config('context') == {}
    assert config.get_config('unknown') == {}
