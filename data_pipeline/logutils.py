from data_pipeline import APP_DIR
from datetime import datetime
import os

LOG_DIR = os.path.join(APP_DIR, "log")


class MissingDataLogger:
    save_file = None
    save_folder = "log"

    def __init__(self, save_path):
        self.save_file = os.path.join(self.save_folder, save_path)

    def log(self, field_name, res_id):
        if not os.path.exists(self.save_folder):
            os.mkdir(self.save_folder)

        with open(self.save_file, 'w') as log_file:
            log_file.write("Can't find section {} for Guest {}.".format(field_name, res_id))
            log_file.close()


class SeleniumLoggerUtil:
    @staticmethod
    def save_screenshot(browser):
        screenshot_name = os.path.join(LOG_DIR, "{}.jpg".format(datetime.now().strftime("%H-%M-%S")))
        browser.save_screenshot(screenshot_name)
