from os import getenv
from locust import HttpUser
from .sitemapSwarmer import SitemapSwarmer


class WebSiteLoad(HttpUser):
    tasks = {
        SitemapSwarmer: 20,
    }
    host = getenv('SITE', 'https://www.example.com')
    min_wait = 5 * 1000
    max_wait = 20 * 1000
