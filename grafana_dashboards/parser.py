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
from collections.abc import Generator, Iterable, Iterator
from typing import Any

import yaml

from grafana_dashboards.components.base import ComponentRegistry
from grafana_dashboards.components.projects import Project
from grafana_dashboards.gdbyaml import GDBLoader

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class DefinitionParser:
    def __init__(self) -> None:
        super().__init__()

    def load_projects(self, paths: Iterable[str]) -> Iterable[Project]:
        registry = ComponentRegistry()
        for path in paths:
            with open(path) as fp:
                for component in self._iter_over_all(yaml.load_all(fp, Loader=GDBLoader)):
                    registry.add(component)
        return registry[Project]

    @staticmethod
    def _iter_over_all(documents: Iterator[Any]) -> Generator[Any, Any, None]:
        return (component
                for document in documents
                for component in document)
