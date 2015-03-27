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
import cgi
from flask import Flask, render_template, jsonify, request

import database
import extractor
import config
import utils

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route('/random')
def main():
    urls = extractor.get_urls()

    return jsonify({'urls': urls})

def init(config_file=None):
    utils.init_logger()
    logger.info('Monobox aggregator server starting up')

    config.init(config_file)
    database.init(config.get('common', 'database_file'))

def run():
    init()
    app.run(host=config.get('server', 'listen_address'),
            port=config.getint('server', 'listen_port'))

if __name__ == '__main__':
    run()

