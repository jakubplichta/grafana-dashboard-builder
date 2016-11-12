# -*- coding: utf-8 -*-
# Copyright 2015-2016 grafana-dashboard-builder contributors
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
import mock

from grafana_dashboards.components.projects import Project

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


def test_project():
    with mock.patch('grafana_dashboards.components.base.ComponentRegistry') as registry:
        data = {
            'project': {
                'dashboards': [
                    'dashboard0',
                    'dashboard1',
                    '{single}',
                    '{dict}',
                    '{list}'
                ],
                'single': 'first',
                'list': [
                    'list0',
                    'list1'
                ],
                'dict': [
                    {
                        'dict0': {
                            'dict-value': '00'
                        }
                    },
                    {
                        'dict1': {
                            'dict-value': '10'
                        }
                    }
                ],
                'wrapped': '{single}',
                'double-wrapped': '{wrapped}'
            }
        }
        mocked_component = mock.Mock()
        registry.get_component = mock.Mock(return_value=mocked_component)
        project = Project(data, registry)

        dashboards = project.get_dashboards()
        assert dashboards is not None
        assert len(dashboards) == 5
        for dashboard in dashboards:
            assert dashboard == mocked_component

        contexts = [context for context in project.get_contexts()]
        assert contexts is not None
        assert len(contexts) == 4
        for context in contexts:
            to_expand = '{single}-{list}-{dict}-{dict-value}-{missing}-{wrapped}-{double-wrapped}'
            expanded = context.expand_placeholders(to_expand)
            assert expanded != to_expand
            assert '{single}' not in expanded
            assert '{list}' not in expanded
            assert '{dict}' not in expanded
            assert '{dict-value}' not in expanded
            assert '{missing}' in expanded
            assert '{wrapped}' not in expanded
            assert '{double-wrapped}' not in expanded
