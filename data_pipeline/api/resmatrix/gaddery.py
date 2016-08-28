from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from data_pipeline.api.resmatrix.events import *
from data_pipeline.common import Gaddery
from data_pipeline.log import MissingDataLogger
from data_pipeline.shortcuts import check_element_exists
from data_pipeline.security import PasswordManager
from data_pipeline.api.resmatrix.htmlprofile import ResMatrixHtmlProfile
from time import sleep


class RsrvTypes:
    arrival = "Arrival"
    booked = "Booked"
    update = "Update"

MAX_PAGES = 64
RSRV_TYPE = RsrvTypes.arrival
OUTPUT_EXCEL = "booking-data-arrivals.xls"
LOG_FILE = "missing-data.log"


class ResMatrixBookingGaddery(Gaddery):
    browser = None
    missing_data_logger = None
    default_start_link = "https://res.travlynx.com/Admin/Login/SignIn.aspx"
    start_date = None
    end_date = None

    def __init__(self, browser, start_date, end_date=None):
        super(ResMatrixBookingGaddery, self).__init__(browser)
        self.start_date = start_date
        if end_date:
            self.end_date = end_date
        else:
            self.end_date = start_date
        self.missing_data_logger = MissingDataLogger(LOG_FILE)

    def get_scraped_data(self):
        self.browser.get(self.default_start_link)
        # new_booking = ResBookingBuilder(filename=OUTPUT_EXCEL)
        # header_names = get_fields_from_profile(ResMatrixHtmlProfile)
        # new_booking.set_header_names(header_names)
        self._login()
        self._select_sidebar_menu_item('Res Detail')
        self._filter_bookings(self.start_date, self.end_date, RSRV_TYPE)
        current_page = 0
        if check_element_exists('ctl00$CPH1$AspNetPager1_input', self.browser):
            MAX_PAGES = len(Select(self.browser.find_element_by_id('ctl00$CPH1$AspNetPager1_input')).options)

            WebDriverWait(self.browser, 3).until(
                TableHasRowQtyEvent(12, current_page, MAX_PAGES))

            while current_page < MAX_PAGES:
                self.__crawl_through_reservation_data()
                page_selector = Select(self.browser.find_element_by_id('ctl00$CPH1$AspNetPager1_input'))
                current_page = int(page_selector.all_selected_options[0].text)
                try:
                    page_selector.select_by_value(str(current_page + 1))
                except NoSuchElementException:
                    break
                self.browser.switch_to_default_content()
                time.sleep(2)
                self.browser.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME)
        else:
            self.__crawl_through_reservation_data()
        return self.scraped_data

    def __crawl_through_reservation_data(self):
        table = self.browser.find_element_by_class_name("data")
        links = []

        for row in table.find_elements_by_tag_name("tr")[2:]:
            res_id = row.find_elements_by_tag_name("td")[1].text
            links.append(res_id)

        for res_id in links:
            WebDriverWait(self.browser, 60).until(
                ElementIsAccessibleEvent(res_id))
            pop_up = self.browser.find_element(By.TAG_NAME, "iframe")
            self.browser.switch_to_frame(pop_up)
            self._gather_data(res_id)
            frame = self.browser.find_element(By.TAG_NAME, "body")
            frame.send_keys(Keys.ESCAPE)
            self.browser.switch_to_default_content()

    def _login(self):
        pw = PasswordManager('resmatrix')
        signin_form = self.browser.find_element_by_id("aspnetForm")

        if signin_form:
            user_textbox = signin_form.find_element_by_id("txtUrs")
            user_textbox.send_keys(pw.get_username())
            pass_textbox = signin_form.find_element_by_id("txtPwd")
            pass_textbox.send_keys(pw.get_password())
            login_btn = signin_form.find_element_by_id("btnLogin")
            login_btn.click()

    def _select_sidebar_menu_item(self, menu_item):
        menu_items = self.browser.find_elements_by_class_name("expandable-hitarea")
        for item in menu_items:
            item.click()
        adddtl_menu_item = self.browser.find_element(By.PARTIAL_LINK_TEXT, menu_item)
        adddtl_menu_item.click()

    def _filter_bookings(self, start_date, end_date, res_type):
        type_selector = Select(self.browser.find_element_by_id('CPH1_ddlDateType'))
        type_selector.select_by_visible_text(res_type)
        begin_date_textbox = self.browser.find_element_by_id('CPH1_txtBeginDate')
        begin_date_textbox.clear()
        begin_date_textbox.send_keys(start_date)
        end_date_textbox = self.browser.find_element_by_id('CPH1_txtEndDate')
        end_date_textbox.clear()
        end_date_textbox.send_keys(end_date)
        search_btn = self.browser.find_element_by_id('CPH1_btnSearch')
        search_btn.click()
        sleep(3)

    def _gather_data(self, res_id):
        profile = ResMatrixHtmlProfile()
        gathered_data = {}
        for tab_name in profile.html_pages.keys():
            try:
                self.browser.find_element_by_link_text(tab_name).click()
                field_list = profile.html_pages[tab_name]
                for element_id, field_name in field_list:
                    try:
                        gathered_data[field_name] = self.browser.find_element_by_css_selector(element_id)\
                            .text.replace("\n", "")
                    except NoSuchElementException:
                        self.missing_data_logger.log(element_id, res_id)
            except NoSuchElementException:
                        self.missing_data_logger.log(tab_name, res_id)
        self.scraped_data.append(gathered_data)

    @staticmethod
    def get_page_time(browser):
        return browser.execute_script("return HotelLocalTime.getMinutes() + HotelLocalTime.getSeconds() + "
                                      "HotelLocalTime.getMilliseconds();")

    class WaitPageUpdatesEvents:
        def __init__(self, browser, current_time):
            self.current_time = current_time
            self.browser = browser

        def __call__(self, *args, **kwargs):
            print(args)
            print(kwargs)
            print(self.current_time, ResMatrixBookingGaddery.get_page_time(self.browser))
            return ResMatrixBookingGaddery.get_page_time(self.browser) != self.current_time
