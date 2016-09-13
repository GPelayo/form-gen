import os
from django.test import TestCase
from selenium.webdriver import Chrome
from formgen import APP_DIR


class MainPageTest(TestCase):
    browser = None

    def setUp(self):
        self.browser = Chrome()
        self.browser.get('http://127.0.0.1')

    def test_website_is_live_for_test(self):
        self.browser.implicitly_wait(100)
        title_name = self.browser.title
        self.assertEqual('Sample UI by Geryl Pelayo', title_name, msg='Please run formgen server at localhost')

    def test_image_generation(self):
        img_asset_path = os.path.join(APP_DIR, 'config', 'assets', 'templates', 'sample.png')
        self.browser.find_element_by_id('id_template_image').send_keys(img_asset_path)

    def tearDown(self):
        self.browser.close()
