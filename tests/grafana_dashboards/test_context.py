# -*- coding: utf-8 -*-
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
from __future__ import unicode_literals

from grafana_dashboards.context import DictDefaultingToPlaceholder, Context

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


def test_dict():
    d = DictDefaultingToPlaceholder({'a': 1})

    assert d['a'] == 1
    assert d['b'] == '{b}'


def test_context_expands_scalar_value():
    data = {
        'single': 'first',
        'wrapped': '{single}',
        'double-wrapped': '{wrapped}'
    }
    contexts = [context for context in Context.create_context(data, keys_to_expand=('expanded-list', 'expanded-dict'))]
    assert len(contexts) == 1
    expected = {
        'double-wrapped': 'first',
        'single': 'first',
        'wrapped': 'first',
        'single-escaped': '{not-expanded}',
        'double-escaped': '{{not-expanded}}'
    }
    to_expand = {
        'single': '{single}',
        'wrapped': '{wrapped}',
        'double-wrapped': '{double-wrapped}',
        'single-escaped': '{{not-expanded}}',
        'double-escaped': '{{{{not-expanded}}}}'
    }
    assert contexts[0].expand_placeholders(to_expand) == expected


def test_context_expands_list_value():
    data = {
        'single': 'first',
        'expanded-list': [
            'list0',
            'list1'
        ]
    }
    contexts = [context for context in Context.create_context(data, keys_to_expand=('expanded-list', 'expanded-dict'))]
    assert len(contexts) == 2
    expected0 = {'single': 'first', 'expanded-list': 'list0'}
    expected1 = {'single': 'first', 'expanded-list': 'list1'}
    to_expand = {'single': '{single}', 'expanded-list': '{expanded-list}'}
    assert contexts[0].expand_placeholders(to_expand) == expected0
    assert contexts[1].expand_placeholders(to_expand) == expected1


def test_context_inserts_list_value():
    data = {
        'single': 'first',
        'inserted-list': [
            'list0',
            'list1'
        ]
    }
    contexts = [context for context in Context.create_context(data, keys_to_expand=('expanded-list', 'expanded-dict'))]
    assert len(contexts) == 1
    expected = {
        'single': 'first',
        'inserted-list': [
            'list0',
            'list1'
        ]
    }
    to_expand = {'single': '{single}', 'inserted-list': '{inserted-list}'}
    assert contexts[0].expand_placeholders(to_expand) == expected


def test_context_expands_dict_value():
    data = {
        'single': 'first',
        'expanded-dict': [
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
        ]
    }
    contexts = [context for context in Context.create_context(data, keys_to_expand=('expanded-list', 'expanded-dict'))]
    assert len(contexts) == 2
    expected0 = {'single': 'first', 'expanded-dict': 'dict0', 'dict-value': '00'}
    expected1 = {'single': 'first', 'expanded-dict': 'dict1', 'dict-value': '10'}
    to_expand = {'single': '{single}', 'expanded-dict': '{expanded-dict}', 'dict-value': '{dict-value}'}
    assert contexts[0].expand_placeholders(to_expand) == expected0
    assert contexts[1].expand_placeholders(to_expand) == expected1
