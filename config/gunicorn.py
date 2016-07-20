#!/usr/bin/env python


import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing


bind = "127.0.0.1:5000"
# bind = 'unix:/var/run/planet.sock'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

timeout = 30

proc_name = 'planet'

accesslog = '-'
loglevel = 'warning'
errorlog = '-'

secure_scheme_headers = {
    'X-FORWARDED-FOR': 'https',
}
