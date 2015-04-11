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

import argparse
import logging
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
    return jsonify({'error_code': 0, 'error_string': '', 'session_id': '1234567890'})

@app.route('/stations')
def stations():
    if not 'session_id' in request.values:
        return jsonify({'error_code': 100, 'error_string': 'missing session_id parameter'})
    
    urls = extractor.get_random_urls()

    return jsonify({'error_code': 0, 'error_string': '', 'urls': urls})

def init(config_file=None):
    utils.init_logging()
    logger.info('Monobox aggregator server starting up')

    config.init(config_file)
    database.init(config.get('common', 'database_file'))

def run():
    init()
    app.run(host=config.get('server', 'listen_address'),
            port=config.getint('server', 'listen_port'))

if __name__ == '__main__':
    run()

