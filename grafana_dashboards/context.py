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
from __future__ import annotations

import itertools
import re
import string
from collections.abc import Container, Generator, Iterable, Mapping
from typing import Any, cast

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


class Context:
    _pattern = re.compile('{.*}')
    _context: Mapping[str, str] | None

    def __init__(self, context: Mapping[str, str] | None = None) -> None:
        super().__init__()
        if not context:
            self._context = None
        else:
            self._context = DictDefaultingToPlaceholder(context)

    def expand_placeholders(self, to_expand: Any) -> Any:
        if not self._context:
            return to_expand

        if isinstance(to_expand, str):
            (result, to_expand) = self._expand(to_expand)
            while result != to_expand:
                (result, to_expand) = self._expand(result)
            if isinstance(result, str):
                return string.Formatter().vformat(result, (), self._context)
            else:
                return result
        elif isinstance(to_expand, list):
            return [self.expand_placeholders(value) for value in to_expand]
        elif isinstance(to_expand, dict):
            return {key: self.expand_placeholders(value) for (key, value) in to_expand.items()}
        else:
            return to_expand

    def _expand(self, to_expand: str | Any) -> tuple[str, str | Any]:
        context = cast(Mapping[str, str], self._context)  # at this point context is always Mapping
        if not isinstance(to_expand, str):
            return to_expand, to_expand
        elif self._pattern.match(to_expand) and to_expand[1:-1] in context:
            return context[to_expand[1:-1]], to_expand
        escaped = to_expand.replace('{{', '{{{{').replace('}}', '}}}}')
        return string.Formatter().vformat(escaped, (), context), to_expand

    def __str__(self) -> str:
        return str(self._context)

    @staticmethod
    def create_context(data: Any, keys_to_expand: Container[str] | None = None) -> Generator[Context, Any, None]:
        return (Context(Context(context).expand_placeholders(context))
                for context in ContextExpander(keys_to_expand).create_context(None, data))


class DictDefaultingToPlaceholder(dict[str, Any]):
    def __missing__(self, key: str) -> str:
        return '{' + key + '}'


class ContextExpander:
    def __init__(self, keys_to_expand: Container[str] | None = None) -> None:
        super().__init__()
        self._keys_to_expand = keys_to_expand if keys_to_expand else []

    def create_context(self, key: object, value: object, parent: object = None) -> Generator[dict[Any, Any], Any, None]:
        contexts: list[Iterable[dict[Any, Any]]] = []
        if isinstance(value, list):
            if key in self._keys_to_expand:
                contexts.append(context for data in value for context in self.create_context(key, data, key))
            else:
                contexts.append(itertools.repeat({key: value}, 1))
        elif isinstance(value, dict):
            for (sub_key, sub_value) in value.items():
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
