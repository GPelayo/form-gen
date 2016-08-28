class DataTarget:
    def __init__(self, css_selector, name):
        self.css_selector = css_selector
        self.name = name


class HTMLProfile:
    html_pages = None

    def __init__(self):
        self.html_pages = {}


class Gaddery:
    gaddery_name = None
    scraped_data = None
    cookie_name = ""
    browser = None
    SCHOOL = "school"
    NAME = "name"
    CURRENT_JOB = "curr_job"
    PREVIOUS_JOB = "prev_job"

    def __init__(self, browser):
        self.browser = browser
        self.scraped_data = []

    def get_scraped_data(self):
        raise NotImplementedError
