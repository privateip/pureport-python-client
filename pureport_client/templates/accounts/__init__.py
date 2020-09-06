# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import urllib

from logging import getLogger

from pureport_client.templates import TemplateBase
from pureport_client.table import render

log = getLogger(__name__)


class Template(TemplateBase):

    def list(self, response):
        cols = ((35, 'id'), (35, 'name'), (10, 'state'))
        self.output(render(cols, response))
