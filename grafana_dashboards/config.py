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
import logging
import os

import yaml

__author__ = 'Jakub Plichta <jakub.plichta@gmail.com>'


logger = logging.getLogger(__name__)


class Config(object):

    def __init__(self, config=None):
        super(Config, self).__init__()
        if not os.path.exists(config):
            logger.debug("Config file '{0}' does not exist".format(config))
            self._config = {}
        else:
            with file(config) as fp:
                self._config = yaml.load(fp)

    def get_config(self, section):
        return self._config.setdefault(section, {})
