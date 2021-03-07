import sys
import gevent
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging

setup_logging("INFO", None)

from .webSiteLoad import WebSiteLoad

def main():
    env = Environment(user_classes=[WebSiteLoad])

    env.create_local_runner()
    if sys.argv[0] == "web-site-load":
        env.create_web_ui()
        print("Open your browser to http://localhost:8089/ to configure/run")
        try:
            env.web_ui.greenlet.join()
        except KeyboardInterrupt:
            env.web_ui.stop()
            print("Terminating")

    if sys.argv[0] == "web-site-run":
        gevent.spawn(stats_printer(env.stats))
        print("Starting 20 users, 10/s")
        env.runner.start(20, spawn_rate=10)
        print("Wait 1 minute and quit...")
        gevent.spawn_later(60, lambda: env.runner.quit())
        try:
            env.runner.greenlet.join()
        except KeyboardInterrupt:
            print("Terminating")

