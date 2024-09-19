import multiprocessing
import os 
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
timeout = 180
bind = "0.0.0.0:" + os.environ.get('PORT', '8000')