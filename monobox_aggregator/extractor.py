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

import database
import config
import random

SC_TUNE_URL='http://yp.shoutcast.com/sbin/tunein-station.pls'

def get_random_sc_urls():
    urls = []
    for station in database.ShoutcastStation.select():
        urls.append('%s?id=%s' % (SC_TUNE_URL, station.scid))

    random.shuffle(urls)

    return urls[0:config.getint('server', 'urls_per_request')]

def get_loved_urls(auth_code):
    return [station.url for station in database.LovedStation.select().where(auth_code==auth_code)]
