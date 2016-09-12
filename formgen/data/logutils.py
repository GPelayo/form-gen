from data import APP_DIR
from datetime import datetime
import os
import logging


LOG_DIR = os.path.join(APP_DIR, "log")

DEFAULT_LEVEL = logging.INFO


class DataLogger:
    def __init__(self, save_path):
        self.logger = logging.getLogger('skipped-data')
        self.logger.setLevel(DEFAULT_LEVEL)
        self.file_name = os.path.join(LOG_DIR, save_path)
        md_formatter = logging.Formatter('%(asctime)s %(message)s')
        md_flhandler = logging.FileHandler(self.file_name)
        md_flhandler.setFormatter(md_formatter)
        self.logger.addHandler(md_flhandler)
        self.save_file = os.path.join(LOG_DIR, save_path)

    def log(self, message, level=DEFAULT_LEVEL):
        if not os.path.exists(LOG_DIR):
            os.mkdir(LOG_DIR)
        self.logger.log(level, message)


class SeleniumLoggerUtil:
    @staticmethod
    def save_screenshot(browser):
        screenshot_name = os.path.join(LOG_DIR, "{}.jpg".format(datetime.now().strftime("%H-%M-%S")))
        browser.save_screenshot(screenshot_name)
