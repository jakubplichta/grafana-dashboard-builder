#!/usr/bin/env python
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

import argparse
import imp
import logging
import os

import yaml

from grafana_dashboards.builder import DashboardBuilder
from grafana_dashboards.parser import DefinitionParser

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
    parser = argparse.ArgumentParser(conflict_handler="resolve")
    parser.add_argument('-p', '--path', required=True, nargs='+', type=str,
                        help='List of path to YAML definition files')
    parser.add_argument('--project',
                        help='(deprecated) Location of the file containing project definition.')
    parser.add_argument('-o', '--out',
                        help='Path to output folder')
    parser.add_argument('--context', default='{}',
                        help='YAML structure defining parameters for dashboard definition.'
                             ' Effectively overrides any parameter defined on project level.')
    parser.add_argument('--plugins', nargs='+', type=str,
                        help='List of external component plugins to load')
    args = parser.parse_args()

    if args.plugins:
        for plugin in args.plugins:
            try:
                imp.load_source('grafana_dashboards.components.$loaded', plugin)
            except Exception as e:
                print 'Cannot load plugin %s: %s' % (plugin, str(e))

    paths = []
    if args.project:
        args.path.append(args.project)
    for path in args.path:
        if os.path.isdir(path):
            for root, dirs, filenames in os.walk(path):
                paths += [os.path.join(root, filename) for filename in filenames]
        else:
            paths.append(path)
    context = yaml.load(args.context)
    projects = DefinitionParser().load_projects(paths)
    builder = DashboardBuilder(args.out)
    for project in projects:
        builder.build_dashboards(project, context)


if __name__ == '__main__':
    main()
