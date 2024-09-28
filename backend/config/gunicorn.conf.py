"""Gunicorn configuration."""
import multiprocessing

bind = "unix:../gunicorn.sock"
logfile = "./gunicorn.log"
loglevel = "error"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 20
threads = 1
