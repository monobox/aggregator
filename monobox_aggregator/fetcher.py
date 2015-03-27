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

import sys
import os
import xml.dom.minidom
import logging
import datetime

import requests

import database
import config
import utils

logger = logging.getLogger(__name__)

class ShoutcastProvider(object):
    def __init__(self):
        sc_file = config.get('fetcher', 'shoutcast_keyfile')
        if not os.path.isfile(sc_file):
            raise RuntimeError('ERROR: SC key file %s not found' % sc_file)
        self.sc_key = open(sc_file).read().strip()

    def get_stations(self, url, additional_params={}):
        data = self.request(url, additional_params)
        if data:
            doc = xml.dom.minidom.parseString(data.encode('utf-8'))
            return doc.getElementsByTagName('station')
        else:
            return None

    def request(self, url, additional_params):
        params = {'k': self.sc_key, 'f': 'xml'}
        params.update(additional_params)
        r = requests.get(url, params=params)

        if r.status_code == 200:
            return r.text
        else:
            return None

def merge_sc_stations(url, listeners_min=0):
    logger.info('Merging shoutcast stations from URL %s' % url)
    sc = ShoutcastProvider()

    stations = sc.get_stations(url)
    merged_count = 0
    for station in stations:
        try:
            old_entry = database.ShoutcastStation.select().where(
                    database.ShoutcastStation.scid==station.getAttribute('id')).get()
        except database.ShoutcastStation.DoesNotExist:
            pass
        else:
            old_entry.delete_instance()

        if int(station.getAttribute('lc')) < listeners_min:
            continue

        station_dbinstance = database.ShoutcastStation.create(
            scid=station.getAttribute('id'),
            name=station.getAttribute('name'),
            lc=station.getAttribute('lc'),
            br=station.getAttribute('br'),
            mt=station.getAttribute('mt'),
            genre=station.getAttribute('genre'),
            ts=datetime.datetime.now())

        station_dbinstance.save()
        merged_count += 1

    logger.info('Fetched %d stations, merged %d, %d total' % (len(stations),
            merged_count, database.ShoutcastStation.select().count()))

def purge_old_stations(timedelta):
    threshold = datetime.datetime.now() - timedelta
    q = database.ShoutcastStation.delete().where(database.ShoutcastStation.ts < threshold)
    num_deleted = q.execute()

    logger.info('Purged %d stations (timedelta=%s)' % (num_deleted, timedelta))

def run():
    logging.basicConfig(level=logging.INFO)
    logger.info('Monobox fetcher starting up')

    config.init()
    database.init(config.get('common', 'database_file'))

    max_age = config.get('fetcher', 'max_age')
    if max_age:
        timedelta = utils.str_to_timedelta(max_age)
        if timedelta is None:
            logger.error('Cannot convert configuration parameter '
                    'max_age (%s) to timedelta' % max_age)
            sys.exit(1)
    else:
        timedelta = None

    urls = config.get('fetcher', 'sc_urls').split(' ')
    listeners_min = config.getint('fetcher', 'listeners_min')
    for url in urls:
        merge_sc_stations(url, listeners_min)

    if timedelta is not None:
        purge_old_stations(timedelta)

if __name__ == '__main__':
    run()
