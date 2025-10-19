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

import errno
import json
import logging
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from grafana_dashboards.components.projects import Project

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'

logger = logging.getLogger(__name__)


class DashboardExporter:
    def __init__(self, **kwargs: dict[str, Any]):
        pass

    def process_dashboard(self, project_name: str, dashboard_name: str, dashboard_data: dict[str, str]) -> None:
        pass


class ProjectProcessor:

    def __init__(self, dashboard_processors: list[DashboardExporter]) -> None:
        super().__init__()
        self._dashboard_processors = dashboard_processors

    def process_projects(self, projects: Iterable[Project], parent_context: dict[str, Any] | None = None) -> None:
        for project in projects:
            logger.info("Processing project '%s'", project.name)
            for context in project.get_contexts(parent_context):
                for dashboard in project.get_dashboards():
                    json_obj = dashboard.gen_json(context)
                    dashboard_name = context.expand_placeholders(dashboard.name)
                    for processor in self._dashboard_processors:
                        processor.process_dashboard(project.name, dashboard_name, json_obj)


class FileExporter(DashboardExporter):

    def __init__(self, output_folder: str) -> None:
        super().__init__()
        self._output_folder = output_folder
        path = Path(self._output_folder)
        if not path.exists():
            path.mkdir(parents=True)
        if not path.is_dir():
            raise Exception(f"'{self._output_folder}' must be a directory")

    def process_dashboard(self, project_name: str, dashboard_name: str, dashboard_data: dict[str, str]) -> None:
        super().process_dashboard(project_name, dashboard_name, dashboard_data)
        dirname = Path(self._output_folder) / project_name
        try:
            dirname.mkdir(parents=True)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        dashboard_path = dirname / f'{dashboard_name}.json'
        logger.info("Saving dashboard '%s' to '%s'", dashboard_name, str(dashboard_path.absolute()))
        with open(dashboard_path, 'w') as f:
            json.dump(dashboard_data, f, sort_keys=True, indent=2, separators=(',', ': '))
