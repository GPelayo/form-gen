import os
import zipfile
import configparser
from django.test import LiveServerTestCase
from selenium.webdriver import Chrome, ChromeOptions
from formgen import APP_DIR as FORMGEN_DIR
import hashlib
from sampleapp.sampleui import APP_DIR
from time import sleep

test_download_folder = os.path.join(APP_DIR, 'test', 'downloads')
zip_filepath = os.path.join(test_download_folder, 'gen.zip')
extracted_dir = os.path.join(test_download_folder, 'gen')

cfg = configparser.ConfigParser()
DEFAULT_IP = 'http://127.0.0.1:8000'
cf_ip_address = cfg.get('Django', 'ip', fallback=DEFAULT_IP)


class MainPageTest(LiveServerTestCase):
    FONT_SIZE_INPUT_ID = 'id_font_size'
    FONT_TYPE_INPUT_ID = 'id_font_type'
    CSV_INPUT_ID = 'id_csv_file'
    TARGET_FIELD_ID = 'id_target_field'
    IMAGE_INPUT_ID = 'id_template_image'
    SUBMIT_BUTTON_ID = 'submit_btn'

    browser = None
    co = ChromeOptions()
    desired_caps = {'download.default_directory': test_download_folder}
    co.add_experimental_option('prefs', desired_caps)
    global cf_ip_address
    site_address = cf_ip_address

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
        # self.browser.execute_script("window.onerror=function(msg){$('body').attr('JSError', msg);}")

    def test_website_is_live_for_test(self):
        self.browser.implicitly_wait(100)
        title_name = self.browser.title
        self.assertEqual('Sample UI by Geryl Pelayo', title_name,
                         msg='Please run formgen server at {}'.format(self.site_address))

    def test_basic_input(self):
        sample_img = os.path.join(FORMGEN_DIR, 'config', 'assets', 'templates', 'sample.png')
        sample_csv = os.path.join(FORMGEN_DIR, 'data', 'api', 'sample', 'dummy-data.csv')
        self.browser.find_element_by_id(self.IMAGE_INPUT_ID).send_keys(sample_img)
        self.browser.find_element_by_id(self.FONT_TYPE_INPUT_ID).send_keys('Courier')
        self.browser.find_element_by_id(self.FONT_SIZE_INPUT_ID).send_keys('22')
        self.browser.find_element_by_id(self.CSV_INPUT_ID).send_keys(sample_csv)
        self.browser.find_element_by_id(self.TARGET_FIELD_ID).send_keys('name')
        self.input_box_selection(214, 232, 398, 275)
        self.browser.find_element_by_class_name(self.SUBMIT_BUTTON_ID).click()
        self.assert_no_django_validation_errors()
        failed_images = self.check_zip_file()
        self.assertTrue(not failed_images, "The following images failed the test.\n" + "\n".join(failed_images))

    def test_no_font_size_input(self):
        test_invalid_field = self.FONT_SIZE_INPUT_ID
        sample_img = os.path.join(FORMGEN_DIR, 'config', 'assets', 'templates', 'sample.png')
        sample_csv = os.path.join(FORMGEN_DIR, 'data', 'api', 'sample', 'dummy-data.csv')
        self.browser.find_element_by_id(self.IMAGE_INPUT_ID).send_keys(sample_img)
        self.browser.find_element_by_id(self.FONT_TYPE_INPUT_ID).send_keys('Courier')
        self.browser.find_element_by_id(self.CSV_INPUT_ID).send_keys(sample_csv)
        self.browser.find_element_by_id(self.TARGET_FIELD_ID).send_keys('name')
        self.input_box_selection(214, 232, 398, 275)
        self.browser.find_element_by_class_name(self.SUBMIT_BUTTON_ID).click()
        self.assert_element_has_html5_validation_error([test_invalid_field])

    def test_no_target_field_input(self):
        test_invalid_field = self.TARGET_FIELD_ID
        sample_img = os.path.join(FORMGEN_DIR, 'config', 'assets', 'templates', 'sample.png')
        sample_csv = os.path.join(FORMGEN_DIR, 'data', 'api', 'sample', 'dummy-data.csv')
        self.browser.find_element_by_id(self.IMAGE_INPUT_ID).send_keys(sample_img)
        self.browser.find_element_by_id(self.FONT_TYPE_INPUT_ID).send_keys('Courier')
        self.browser.find_element_by_id(self.FONT_SIZE_INPUT_ID).send_keys('22')
        self.browser.find_element_by_id(self.CSV_INPUT_ID).send_keys(sample_csv)
        self.input_box_selection(214, 232, 398, 275)
        self.browser.find_element_by_class_name(self.SUBMIT_BUTTON_ID).click()
        self.assert_element_has_html5_validation_error([test_invalid_field])

    def input_box_selection(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        with open(os.path.join(APP_DIR, 'fireboxselect.js'), 'r') as jsfile:
            self.browser.execute_script(jsfile.read(), top_left_x, top_left_y, bottom_right_x, bottom_right_y)

    def assert_no_django_validation_errors(self):
        error_count = len(self.browser.find_elements_by_css_selector("ul.errorlist li"))
        self.assertEqual(error_count, 0, "There are {} errors.".format(error_count))

    def assert_element_has_html5_validation_error(self, fields: list):
        invalid_input_list = self.browser.find_elements_by_css_selector("input:invalid")
        self.assertEqual(len(invalid_input_list), len(fields))
        for field_input in fields:
            for invalid_input in invalid_input_list:
                self.assertEqual(invalid_input.get_attribute('id'), field_input,
                                 "Element {} doesn't correctly validate input".format(field_input))

    def check_zip_file(self):
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
        return failed_images

    def tearDown(self):
        self.browser.close()
