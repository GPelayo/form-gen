from selenium.common.exceptions import NoSuchElementException


def check_element_exists(element_id, browser):
    try:
        browser.find_element_by_id(element_id)
    except NoSuchElementException:
        return False
    return True
