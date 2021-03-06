from locust.env import Environment

from .webSiteLoad import WebSiteLoad

env = Environment(user_classes=[WebSiteLoad])

env.create_local_runner()
env.create_web_ui()
print("Open your browser to http://localhost:8089/ to configure/run")
try:
    env.web_ui.greenlet.join()
except KeyboardInterrupt:
    print("Terminating")
