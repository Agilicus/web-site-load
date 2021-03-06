import random
from locust import TaskSet, task
from pyquery import PyQuery


class SitemapSwarmer(TaskSet):
    def on_start(self):
        request = self.client.get("/robots.txt")
        self.sitemap_links = ['/']
        for line in request.content.decode('utf-8').split("\n"):
            fn = line.split()[:1]
            if len(fn) and fn[0] == "Sitemap:":
                lf = line.split()[1:][0]
                request = self.client.get(lf)
                pq = PyQuery(request.content, parser='html')
                for loc in pq.find('loc'):
                    self.sitemap_links.append(PyQuery(loc).text())
        self.sitemap_links = list(set(self.sitemap_links))

    @task(10)
    def load_page(self):
        url = random.choice(self.sitemap_links)
        self.client.get(url)
