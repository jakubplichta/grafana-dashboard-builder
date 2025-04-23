# -*- coding: utf-8 -*-
# Copyright 2015-2019 grafana-dashboard-builder contributors
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
from __future__ import unicode_literals

import importlib.machinery
import importlib.util
import re
import sys

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


_first_cap_re = re.compile('(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')


def get_component_type(clazz):
    """

    :type clazz: type
    """
    return _all_cap_re.sub(r'\1-\2', _first_cap_re.sub(r'\1-\2', clazz.__name__)).lower()


if sys.version_info >= (3, 12):
    def load_source(modname, filename):
        loader = importlib.machinery.SourceFileLoader(modname, filename)
        spec = importlib.util.spec_from_file_location(modname, filename, loader=loader)
        module = importlib.util.module_from_spec(spec)

        loader.exec_module(module)
        return module
else:
    from imp import load_source
