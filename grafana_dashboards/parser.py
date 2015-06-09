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

import yaml

from grafana_dashboards.components.base import ComponentRegistry
from grafana_dashboards.components.projects import Project

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class DefinitionParser(object):
    def __init__(self):
        super(DefinitionParser, self).__init__()

    def load_projects(self, paths):
        registry = ComponentRegistry()
        for path in paths:
            with file(path, 'r') as fp:
                for component in self._iter_over_all(yaml.load_all(fp)):
                    registry.add(component)
        return registry[Project]

    @staticmethod
    def _iter_over_all(documents):
        return (component
                for document in documents
                for component in document)
