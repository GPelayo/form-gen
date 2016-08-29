from selenium.common.exceptions import WebDriverException

import time


class TableHasRowQtyEvent:
    count = -1
    current_page = -1
    max_pages = -1

    def __init__(self, count, current_page, max_pages):
        self.count = count
        self.current_page = current_page
        self.max_pages = max_pages

    def __call__(self, driver):
        if self.current_page == self.max_pages:
            time.sleep(3)
            return True
        try:
            row_count = len(driver.find_element_by_tag_name("table").find_elements_by_tag_name("tr"))
            return self.count == row_count
        except Exception as e:
            print(e)


class ElementIsAccessibleEvent:
    id = None

    def __init__(self, tag_id):
        self.id = tag_id

    def __call__(self, driver):
        try:
            table = driver.find_element_by_class_name("data")
            table.find_element_by_link_text(self.id).click()
            return True
        except WebDriverException as e:
            print(e.msg)
            pass


class ValuesAreEqual:
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2

    def __call__(self, driver):
        return self.value1 == self.value2
