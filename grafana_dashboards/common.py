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
import importlib.machinery
import importlib.util
import re

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'

from types import ModuleType

_first_cap_re = re.compile('(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')


def get_component_type(clazz: type) -> str:
    return _all_cap_re.sub(r'\1-\2', _first_cap_re.sub(r'\1-\2', clazz.__name__)).lower()


# Replacement to imp.load_source suggested on the python 3.12 changelog:
# https://docs.python.org/3/whatsnew/3.12.html#imp
def load_source(modname: str, filename: str) -> ModuleType:
    loader = importlib.machinery.SourceFileLoader(modname, filename)
    spec = importlib.util.spec_from_file_location(modname, filename, loader=loader)
    module = importlib.util.module_from_spec(spec)  # type: ignore

    loader.exec_module(module)
    return module
