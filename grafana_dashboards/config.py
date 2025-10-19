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

import logging
from pathlib import Path
from typing import Any

import yaml

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


logger = logging.getLogger(__name__)


class Config:
    _config: dict[str, Any]

    def __init__(self, config: str | None = None) -> None:
        super().__init__()
        if not config:
            logger.debug("No config file specified")
            self._config = {}
        elif not Path(config).exists():
            logger.debug("Config file '%s' does not exist", config)
            self._config = {}
        else:
            with open(config) as fp:
                self._config = yaml.load(fp, Loader=yaml.FullLoader)

    def get_config(self, section: str) -> dict[str, Any]:
        return self._config.setdefault(section, {})
