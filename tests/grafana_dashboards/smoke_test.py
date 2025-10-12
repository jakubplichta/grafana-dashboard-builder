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

import grafana_dashboards.cli as cli
from grafana_dashboards.config import Config


class DummyExporter(object):

    def __init__(self, prop, **kwargs):
        super().__init__()
        self.prop = prop
        self.kwargs = kwargs


config_file = Path(__file__).resolve().parent / 'config.yaml'
config = Config(config_file)
# noinspection PyProtectedMember
exporters = cli._initialize_exporters('dummy', [DummyExporter], config)

assert exporters is not None
assert len(exporters) == 1
assert exporters[0].prop == 'value'
assert exporters[0].kwargs == {'other': True}
