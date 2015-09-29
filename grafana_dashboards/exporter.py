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

import json
import os
import errno

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class DashboardExporter(object):

    def process_dashboard(self, project_name, dashboard_name, dashboard_data):
        pass


class ProjectProcessor(object):

    def __init__(self, dashboard_processors):
        """

        :type dashboard_processors: list[grafana_dashboards.builder.DashboardExporter]
        """
        super(ProjectProcessor, self).__init__()
        self._dashboard_processors = dashboard_processors

    def process_projects(self, projects, parent_context=None):
        """

        :type projects: list[grafana_dashboards.components.projects.Project]
        :type parent_context: dict
        """
        for project in projects:
            for context in project.get_contexts(parent_context):
                for dashboard in project.get_dashboards():
                    json_obj = dashboard.gen_json(context)
                    dashboard_name = context.expand_placeholders(dashboard.name)
                    for processor in self._dashboard_processors:
                        processor.process_dashboard(project.name, dashboard_name, json_obj)


class FileExporter(DashboardExporter):

    def __init__(self, output_folder):
        super(DashboardExporter, self).__init__()
        self._output_folder = output_folder
        if not os.path.exists(self._output_folder):
            os.makedirs(self._output_folder)
        if not os.path.isdir(self._output_folder):
            raise Exception("'{0}' must be a directory".format(self._output_folder))

    def process_dashboard(self, project_name, dashboard_name, dashboard_data):
        super(FileExporter, self).process_dashboard(project_name, dashboard_name, dashboard_data)
        dirname = os.path.join(self._output_folder, project_name)
        try:
            os.makedirs(dirname)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        dashboard_path = os.path.join(dirname, dashboard_name + '.json')
        with file(dashboard_path, 'w') as f:
            json.dump(dashboard_data, f, sort_keys=True, indent=2, separators=(',', ': '))
