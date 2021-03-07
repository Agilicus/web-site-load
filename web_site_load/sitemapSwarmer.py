import os
import random
from locust import TaskSet, task
from pyquery import PyQuery

class SitemapSwarmer(TaskSet):
    def get_links(self, url):
        links = []
        request = self.client.get(url)
        pq = PyQuery(request.content, parser='html')
        for loc in pq.find('loc'):
            #/category-sitemap.xml
            link = PyQuery(loc).text()
            if os.path.splitext(link)[1] == ".xml":
                links.extend(self.get_links(link))
            else:
                links.append(link)
        return links

    def on_start(self):
        request = self.client.get("/robots.txt")
        self.sitemap_links = self.get_links("/sitemap_index.xml")
        for line in request.content.decode('utf-8').split("\n"):
            fn = line.split()[:1]
            if len(fn) and fn[0] == "Sitemap:":
                lf = line.split()[1:][0]
                self.sitemap_links.extend(self.get_links(lf))

        self.sitemap_links = list(set(self.sitemap_links))

    @task(10)
    def load_page(self):
        url = random.choice(self.sitemap_links)
        self.client.get(url)
