import requests


class HTMLProfile:
    html_pages = None

    def __init__(self):
        self.html_pages = {}


class Gaddery:
    def collect_data(self):
        raise NotImplementedError


class SeleniumGaddery:
    scraped_data = None
    browser = None

    def __init__(self, browser):
        self.browser = browser
        self.scraped_data = []


class ApiGaddery:
    user_agent = None
    client_id = None
    client_secret = None
    username = None
    password = None
