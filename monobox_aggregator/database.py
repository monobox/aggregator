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
import json
import logging

logger = logging.getLogger(__name__)

class FileDatabase(object):
    def __init__(self, filename):
        logger.info('Opening db %s' % filename)
        self.filename = filename
        if os.path.exists(filename):
            self.data = json.load(open(filename))
        else:
            logger.warning('Initializing a new db')
            self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data.get(key, None)

    def commit(self):
        json.dump(self.data, open(self.filename, 'w'))

if __name__ == '__main__':
    db = FileDatabase('db.json')
    print db['testkey']
    db['testkey'] = 1
    db.commit()
