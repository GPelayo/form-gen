import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
CHROME_DRIVER_FILEPATH = os.path.join(APP_DIR, "api", "drivers", "chromedriver.exe")
PHANTOM_JS_FILEPATH = os.path.join(APP_DIR, "api", "drivers", "phantomjs.exe")
