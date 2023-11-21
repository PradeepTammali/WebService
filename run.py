# -*- coding: utf-8 -*-
""" Application loader

This small file is responsible for starting the application with multiple tools:

`python run.py`

"""
import os

from omdb.app import create_app
from omdb.log import log

app = create_app('omdb')

if __name__ == '__main__':
    threaded = bool(os.environ.get('THREADED', False))
    log.info('Threaded: %s', threaded)
    app.run(port=6000, threaded=threaded)
