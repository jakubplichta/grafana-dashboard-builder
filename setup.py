#!/usr/bin/env python
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
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex

        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


params = {
    'name': 'grafana-dashboard-builder',
    'version': '0.4.0a1',
    'packages': [
        'grafana_dashboards',
        'grafana_dashboards.client',
        'grafana_dashboards.components'
    ],
    'scripts': [
        'bin/grafana_dashboard_builder.py'
    ],
    'url': 'https://github.com/jakubplichta/grafana-dashboard-builder',
    'license': 'Apache License, Version 2.0',
    'author': 'Jakub Plichta',
    'author_email': 'jakub.plichta@gmail.com',
    'description': 'Generate Grafana dashboards with YAML',
    'classifiers': [
        'Topic :: Utilities',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    'keywords': 'grafana yaml graphite prometheus influxdb',
    'cmdclass': {'test': Tox},
    'tests_require': ['tox', 'mock'],
    'install_requires': ['PyYAML', 'argparse', 'requests-kerberos', 'requests'],
    'entry_points': {
        'console_scripts': [
            'grafana-dashboard-builder = grafana_dashboards.cli:main',
        ],
    },
    'long_description':
        """grafana-dashboard-builder is an open-source tool for easier creation of Grafana dashboards.
It is written in Python and uses YAML descriptors for dashboard
templates.

This project has been inspired by Jenkins Job Builder that
allows users to describe Jenkins jobs with human-readable format. grafana-dashboard-builder
aims to provide similar simplicity to Grafana dashboard creation and to give users easy way how they can create
dashboard templates filled with different configuration."""
}

setup(**params)
