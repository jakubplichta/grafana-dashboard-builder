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


class DashboardJSONEncoder(json.JSONEncoder):
    def __init__(self):
        super(DashboardJSONEncoder, self).__init__(sort_keys=True, indent=2, separators=(',', ': '))


class DashboardBuilder(object):
    def __init__(self, output_folder):
        super(DashboardBuilder, self).__init__()
        self.output_folder = output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if not os.path.isdir(output_folder):
            raise Exception('out must be a directory')

    def build_dashboards(self, project, context=None):
        """

        :type project: grafana_dashboards.components.Project
        """
        for context in project.get_contexts(context):
            for dashboard in project.get_dashboards():
                json_obj = dashboard.gen_json(context)
                dirname = os.path.join(self.output_folder, project.name)
                try:
                    os.makedirs(dirname)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
                dashboard_path = os.path.join(dirname, context.expand_placeholders(dashboard.name) + '.json')
                with file(dashboard_path, 'w') as f:
                    json.dump(json_obj, f, sort_keys=True, indent=2, separators=(',', ': '))
