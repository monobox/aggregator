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

import logging
import random
import datetime
import uuid
from flask import Flask, jsonify, request

import database
import extractor
import config
import utils

logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error_code': 404, 'error_string': 'resource not found'})

@app.route('/')
def root():
    return ''

@app.route('/register', methods=['POST'])
def register():
    if not 'auth_code' in request.values:
        return jsonify({'error_code': 100, 'error_string': 'missing auth_code parameter'})

    auth_code = request.values['auth_code']
    try:
        database.RegisteredBox.get(database.RegisteredBox.auth_code==auth_code)
    except database.RegisteredBox.DoesNotExist:
        return jsonify({'error_code': 200, 'error_string': 'unregistered auth_code'})

    try:
        session = database.Session.get(database.Session.auth_code==auth_code)
        session.ts = datetime.datetime.now()
        session.save()
        logger.info('Refreshed session %s (auth_code: %s)' % (session.session_id, session.auth_code))
    except database.Session.DoesNotExist:
        session = database.Session.create(auth_code=auth_code, session_id=uuid.uuid4(), ts=datetime.datetime.now())
        session.save()
        logger.info('Created new session %s (auth_code: %s)' % (session.session_id, session.auth_code))

    return jsonify({'error_code': 0, 'error_string': '', 'session_id': session.session_id})

@app.route('/stations')
def stations():
    if not 'session_id' in request.values:
        return jsonify({'error_code': 300, 'error_string': 'missing session_id parameter'})

    try:
        session = database.Session.get(database.Session.session_id==request.values['session_id'])
    except database.Session.DoesNotExist:
        return jsonify({'error_code': 400, 'error_string': 'expired or non-existent session'})

    urls = extractor.get_random_sc_urls()
    loved_urls = extractor.get_loved_urls(session.auth_code)

    logger.info('Merging %d loved urls among %d SC stations' % (len(loved_urls), len(urls)))

    urls += loved_urls

    random.shuffle(urls)

    return jsonify({'error_code': 0, 'error_string': '', 'urls': urls})

def init(config_file=None):
    utils.init_logging()
    logger.info('Monobox aggregator server starting up')

    config.init(config_file)
    database.init(config.get('common', 'database_uri'))

def run():
    init()
    app.run(host=config.get('server', 'listen_address'),
            port=config.getint('server', 'listen_port'))

if __name__ == '__main__':
    run()

