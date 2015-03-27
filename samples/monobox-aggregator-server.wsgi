#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
# Copyright (c) 2015 by OXullo Intersecans / bRAiNRAPERS

from __future__ import unicode_literals

import os
import monobox_aggregator.server

if not 'MONOBOX_AGGREGATOR_CONFIG' in os.environ:
    raise RuntimeError('Environment variable MONOBOX_AGGREGATOR_CONFIG not set')

config_file = os.environ['MONOBOX_AGGREGATOR_CONFIG']

if not os.path.isfile(config_file):
    raise RuntimeError('Cannot find file %s' % config_file)

monobox_aggregator.server.init(config_file)

application = monobox_aggregator.server.app
