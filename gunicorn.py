import os
import multiprocessing

workers = (2 * multiprocessing.cpu_count()) + 1
threads = (4 * multiprocessing.cpu_count())

worker_class = "gevent"
worker_connections = 1024

bind = f'{os.getenv("FLASK_RUN_HOST")}:{os.getenv("FLASK_RUN_PORT")}'
