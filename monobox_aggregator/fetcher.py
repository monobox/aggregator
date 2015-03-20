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
import datetime

import requests

import database
import config

logger = logging.getLogger(__name__)

SC_RANDOM_URL='http://api.shoutcast.com/station/randomstations'

class ShoutcastProvider(object):
    def __init__(self):
        sc_file = config.get('aggregator', 'shoutcast_keyfile')
        if not os.path.isfile(sc_file):
            raise RuntimeError('ERROR: SC key file %s not found' % sc_file)
        self.sc_key = open(sc_file).read().strip()

    def get_random_stations(self, additional_params={}):
        data = self.request(SC_RANDOM_URL, additional_params)
        if data['response']['statusCode'] == 200:
            return data['response']['data']['stationlist']['station']

    def request(self, url, additional_params):
        params = {'k': self.sc_key, 'f': 'json'}
        params.update(additional_params)
        r = requests.get(url, params=params)

        return r.json()

def run():
    logging.basicConfig(level=logging.INFO)
    logger.info('Monobox fetcher starting up')

    config.init()
    database.init(config.get('aggregator', 'database_file'))

    sc = ShoutcastProvider()

    stations = sc.get_random_stations()
    for station in stations:
        try:
            old_entry = database.ShoutcastStation.select().where(
                    database.ShoutcastStation.scid==station['id']).get()
        except database.ShoutcastStation.DoesNotExist:
            pass
        else:
            old_entry.delete_instance()

        station_dbinstance = database.ShoutcastStation.create(
            scid=station['id'],
            name=station['name'],
            lc=station['lc'],
            br=station['br'],
            mt=station['mt'],
            genre=station['genre'],
            ts=datetime.datetime.now())

        station_dbinstance.save()

    logger.info('Fetched %d stations into %d total' % (len(stations),
            database.ShoutcastStation.select().count()))

if __name__ == '__main__':
    run()
