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
import requests

import database
import config

logger = logging.getLogger(__name__)

SC_RANDOM_URL='http://api.shoutcast.com/station/randomstations'
DEV_KEY=open(os.path.join(os.path.dirname(__file__), 'scdev.key')).read().strip()

class ShoutcastProvider(object):
    def __init__(self):
        pass

    def random_request(self, additional_params={}):
        return self.request(SC_RANDOM_URL, additional_params)

    def local_request(self, filename):
        return json.load(open(filename))

    def request(self, url, additional_params):
        params = {'k': DEV_KEY, 'f': 'json'}
        params.update(additional_params)
        r = requests.get(url, params=params)

        return r.json()

class ShoutcastProcessor(object):
    def extract_station_ids(self, data):
        station_ids = list(set([station['id']
                for station in data['response']['data']['stationlist']['station']]))

        return station_ids

def run():
    logging.basicConfig(level=logging.INFO)
    logger.info('Monobox fetcher starting up')

    sc = ShoutcastProvider()
    sp = ShoutcastProcessor()
    db = database.FileDatabase(config.get('aggregator', 'database_file'))

    # station_ids = sp.extract_station_ids(sc.local_request('../tools/stations.json'))
    station_ids = sp.extract_station_ids(sc.random_request())

    db['shoutcast'] = {'station_ids': station_ids,
            'tune_url': 'http://yp.shoutcast.com/sbin/tunein-station.pls'}
    db.commit()

if __name__ == '__main__':
    run()
