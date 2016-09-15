import os
import zipfile
from django.test import TestCase
from selenium.webdriver import Chrome, ChromeOptions
from formgen import APP_DIR as FORMGEN_DIR
import hashlib
from sampleui import APP_DIR
from time import sleep

test_download_folder = os.path.join(APP_DIR, 'test', 'downloads')
zip_filepath = os.path.join(test_download_folder, 'gen.zip')
extracted_dir = os.path.join(test_download_folder, 'gen')


class MainPageTest(TestCase):
    browser = None
    co = ChromeOptions()
    desired_caps = {'download.default_directory': test_download_folder}
    co.add_experimental_option('prefs', desired_caps)
    site_address = 'http://192.168.1.109'

    file_hashes = {'Charlie Lange.jpg': '09cfa0536d62a0e45439d6020b83466179ba899aca8d98c0cd37c4958286aac9',
                   'Lisa Tragnetti.jpg': 'e90233a54dbd4e3593d2758c9ca2d8372c16c5738b8e1cd1009afe94d44308c4',
                   'Maggie Hart.jpg': 'e505720f2ac0e4f831d4f009004ce03a67eae02cc2d1561ea21c6212198afaac',
                   'Marty Hart.jpg': '8324e5c946374d2dedace192cf62af824fd9ee6e1c5974c535a262f46a6ebc69',
                   'Rust Cohle.jpg': 'fd5629acb1812020f71bcb1b37352a76d3b5fcc1bf9d5f012d301c319b269ba4'}

    def setUp(self):
        if os.path.exists(zip_filepath):
            os.remove(zip_filepath)
        self.browser = Chrome(chrome_options=self.co)
        self.browser.get(self.site_address)
        self.browser.execute_script("window.onerror=function(msg){$('body').attr('JSError', msg);}")

    def test_website_is_live_for_test(self):
        self.browser.implicitly_wait(100)
        title_name = self.browser.title
        self.assertEqual('Sample UI by Geryl Pelayo', title_name,
                         msg='Please run formgen server at {}'.format(self.site_address))

    def test_basic_input(self):
        top_left_x = 214
        top_left_y = 232
        bottom_right_x = 398
        bottom_right_y = 275

        sample_img = os.path.join(FORMGEN_DIR, 'config', 'assets', 'templates', 'sample.png')
        sample_csv = os.path.join(FORMGEN_DIR, 'data', 'api', 'sample', 'dummy-data.csv')
        self.browser.find_element_by_id('id_template_image').send_keys(sample_img)
        self.browser.find_element_by_id('id_font_type').send_keys('Courier')
        self.browser.find_element_by_id('id_font_size').send_keys('22')
        self.browser.find_element_by_id('id_csv_file').send_keys(sample_csv)
        self.browser.find_element_by_id('id_target_field').send_keys('name')

        with open(os.path.join(APP_DIR, 'fireboxselect.js'), 'r') as jsfile:
            self.browser.execute_script(jsfile.read(), top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        self.browser.find_element_by_class_name('submit_btn').click()

        while True:
            if os.path.exists(zip_filepath):
                break
            else:
                sleep(3)

        with open(zip_filepath, 'rb') as zfile:
            zip_obj = zipfile.ZipFile(zfile)
            zip_obj.extractall(extracted_dir)

        failed_images = []
        for file in os.listdir(extracted_dir):
            with open(os.path.join(extracted_dir, file), 'rb') as zfile:
                size = 65536
                hasher = hashlib.sha256()
                bf = zfile.read(size)
                while len(bf) > 0:
                    hasher.update(bf)
                    bf = zfile.read(size)
            hash = hasher.hexdigest()
            if self.file_hashes[file] != hash:
                failed_images.append(file)
        self.assertTrue(not failed_images, "The following images failed the test.\n" + "\n".join(failed_images))

    def tearDown(self):
        self.browser.close()
