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
import peewee
import playhouse.db_url
import logging

logger = logging.getLogger(__name__)

db = peewee.Proxy()

class BaseModel(peewee.Model):
    class Meta:
        database = db

class ShoutcastStation(BaseModel):
    scid = peewee.IntegerField(unique=True)
    name = peewee.TextField()
    lc = peewee.IntegerField()
    br = peewee.IntegerField()
    mt = peewee.TextField()
    genre = peewee.TextField()
    ts = peewee.DateTimeField()

class LovedStation(BaseModel):
    auth_code = peewee.TextField()
    url = peewee.TextField()

class Session(BaseModel):
    auth_code = peewee.TextField()
    session_id = peewee.TextField()
    ts = peewee.DateTimeField()

class RegisteredBox(BaseModel):
    auth_code = peewee.TextField()


def init(uri):
    logger.info('Opening db at %s' % uri)
    db_connection = playhouse.db_url.connect(uri)
    db.initialize(db_connection)
    db.create_tables([ShoutcastStation, LovedStation, Session, RegisteredBox], safe=True)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    init('sqlite://test.db')
