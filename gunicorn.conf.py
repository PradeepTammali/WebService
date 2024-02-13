# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

import multiprocessing

from omdb.app import create_app

# Server socket
bind = '0.0.0.0:8000'
proc_name = 'application'

# Debugging
reload = False
debug = False

# Worker processes
# Using the sync worker_class, you should aim to use 2-4 x $(NUM_CORES) workers
# Using the gevent worker_class, you can increase the number of workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'

# Server mechanics
umask = 0o027

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'


def on_starting(server):  # pylint: disable=unused-argument
    return create_app('db')
