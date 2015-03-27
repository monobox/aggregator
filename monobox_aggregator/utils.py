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

import re
from datetime import timedelta

# http://stackoverflow.com/questions/4628122/how-to-construct-a-timedelta-object-from-a-simple-string
def str_to_timedelta(time_str):

    regex = re.compile(r'((?P<hours>\d+?)h)?\s*((?P<minutes>\d+?)m)?\s*((?P<seconds>\d+?)s)?')

    parts = regex.match(time_str)

    if not parts:
        return None

    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.iteritems():
        if param:
            time_params[name] = int(param)

    return timedelta(**time_params)

if __name__ == '__main__':
    print parse_time('1h24m3s')
    print parse_time('1h 24m 3s')
