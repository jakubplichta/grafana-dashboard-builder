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
import string
import itertools

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class Context(object):

    def __init__(self, context=None):
        super(Context, self).__init__()
        if not context:
            context = {}
        self._context = DictDefaultingToPlaceholder(context)

    def expand_placeholders(self, to_expand):
        """

        :rtype : dict
        """
        if isinstance(to_expand, str):
            formatter = string.Formatter()
            (result, to_expand) = (formatter.vformat(to_expand, (), self._context), to_expand)
            while result != to_expand:
                (result, to_expand) = (formatter.vformat(result, (), self._context), result)
            return result
        elif isinstance(to_expand, list):
            return [self.expand_placeholders(value) for value in to_expand]
        elif isinstance(to_expand, dict):
            return dict([(key, self.expand_placeholders(value)) for (key, value) in to_expand.iteritems()])
        else:
            return to_expand

    def __str__(self):
        return str(self._context)

    @staticmethod
    def create_context(data, keys_to_expand=None):
        return (Context(Context(context).expand_placeholders(context))
                for context in ContextExpander(keys_to_expand).create_context(None, data))


class DictDefaultingToPlaceholder(dict):
    def __missing__(self, key):
        return '{' + key + '}'


class ContextExpander(object):
    def __init__(self, keys_to_expand=None):
        super(ContextExpander, self).__init__()
        self._keys_to_expand = keys_to_expand if keys_to_expand else []

    def create_context(self, key, value, parent=None):
        contexts = []
        if isinstance(value, list):
            if key in self._keys_to_expand:
                contexts.append((context for data in value for context in self.create_context(key, data, key)))
        elif isinstance(value, dict):
            for (sub_key, sub_value) in value.iteritems():
                if parent and len(value) == 1:
                    contexts.append(self.create_context(parent, sub_key))
                contexts.append(self.create_context(sub_key, sub_value))
        else:
            contexts.append(itertools.repeat({key: value}, 1))
        for context in itertools.product(*contexts):
            result = {}
            multi = {}
            for context_part in context:
                if len(context_part) == 1:
                    result.update(context_part)
                else:
                    multi.update(context_part)
            result.update(multi)
            yield result
