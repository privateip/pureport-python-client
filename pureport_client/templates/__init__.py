# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import urllib

from logging import getLogger

log = getLogger(__name__)


class TemplateBase(object):

    def __init__(self):
        self._lines = list()

    def render(self):
        log.debug("invokving render()")
        return "\n".join(self._lines)

    def output(self, string, variables=None):
        variables = variables or {}
        self._lines.append(string.format(**variables))
