from PIL import ImageFont
from image.drawer import DocumentTemplate, DocumentDrawer
import phonenumbers
from datetime import datetime
from data_pipeline.api.resmatrix.gaddery import ResMatrixBookingGaddery
from selenium.webdriver import Chrome
import os
import json


def brute_test():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "data_pipeline", "api", "drivers", "chromedriver.exe")
    browser = Chrome(path)

    booking_date = "8/19/16"
    end_date = "8/27/16"
    gd = ResMatrixBookingGaddery(browser, booking_date, end_date)
    data = gd.get_scraped_data()

    with open('itr.json', 'w+') as test_file:
        json.dump(data, test_file)

    with open('itr.json', 'r') as test_file:
        data = json.load(test_file)

    default_font_loc = 'font/cour.ttf'

    file_path = "C:\\Users\\Geryl\\PycharmProjects\\form-gen\\form_gen\\assets\\templates\\registration.png"
    template = DocumentTemplate("registration", file_path)

    font = ImageFont.truetype(default_font_loc, 22)
    template.add_output_area("name", 160, 241, font)
    template.add_output_area("street", 155, 306, font)
    template.add_output_area("city", 140, 371, font)
    template.add_output_area("area code", 158, 431, font)
    template.add_output_area("phone number", 212, 431, font)
    template.add_output_area("date in", 1006, 304, font)
    template.add_output_area("date out", 1014, 357, font)
    template.add_output_area("total days", 1050, 412, font)
    template.add_output_area("room rate", 1027, 462, font)
    template.add_output_area("room total", 1040, 515, font)
    template.add_output_area("tax", 995, 568, font)

    for gd in data:
        doc = DocumentDrawer(template)
        full_name = "{} {}".format(gd["first_name"], gd["last_name"])
        street = gd["street"]
        city = gd["city"]

        pn_pbj = phonenumbers.parse(gd["phone_number"], "US")
        if phonenumbers.is_valid_number_for_region(pn_pbj, "US") and \
                (not gd["country"] or gd["country"] == "US"):
            area_code = str(pn_pbj.national_number)[:3]
            phone_number = str(pn_pbj.national_number)[4:]
        else:
            area_code = ""
            phone_number = gd["phone_number"]

        date_in = gd["date_in"]
        date_out = gd["date_out"]
        td_dt = datetime.strptime(date_out, "%m/%d/%Y") - datetime.strptime(date_in, "%m/%d/%Y")
        total_days = str(td_dt.days)
        room_rate = gd["room_rate"].strip('$')
        room_total = gd["room_total"].strip('$')
        room_taxes = gd["room_taxes"].strip('$')

        doc.set_form_data("name", full_name)
        doc.set_form_data("street", street)
        doc.set_form_data("city", city)
        doc.set_form_data("area code", area_code)
        doc.set_form_data("phone number", phone_number)
        doc.set_form_data("date in", date_in)
        doc.set_form_data("date out", date_out)
        doc.set_form_data("total days", total_days)
        doc.set_form_data("room rate", room_rate)
        doc.set_form_data("room total", room_total)
        doc.set_form_data("tax", room_taxes)
        doc.save_image(full_name, open_preview=True)


template = DocumentTemplate('sample')
drawer = DocumentDrawer(template)

# base_dir = os.path.dirname(os.path.abspath(__file__))
# path = os.path.join(base_dir, "data_pipeline", "api", "drivers", "chromedriver.exe")
# browser = Chrome(path)
#
# booking_date = "8/19/16"
# end_date = "8/27/16"
# gd = ResMatrixBookingGaddery(browser, booking_date, end_date)
# data = gd.get_scraped_data()
#
# with open('itr.json', 'w+') as test_file:
#     json.dump(data, test_file)

with open('itr.json', 'r') as test_file:
    data = json.load(test_file)

default_font_loc = 'font/cour.ttf'


for gd in data:
    full_name = "{} {}".format(gd["first_name"], gd["last_name"])
    street = gd["street"]
    city = gd["city"]

    pn_pbj = phonenumbers.parse(gd["phone_number"], "US")
    if phonenumbers.is_valid_number_for_region(pn_pbj, "US") and \
            (not gd["country"] or gd["country"] == "US"):
        area_code = str(pn_pbj.national_number)[:3]
        phone_number = str(pn_pbj.national_number)[4:]
    else:
        area_code = ""
        phone_number = gd["phone_number"]

    date_in = gd["date_in"]
    date_out = gd["date_out"]
    td_dt = datetime.strptime(date_out, "%m/%d/%Y") - datetime.strptime(date_in, "%m/%d/%Y")
    total_days = str(td_dt.days)
    room_rate = gd["room_rate"].strip('$')
    room_total = gd["room_total"].strip('$')
    room_taxes = gd["room_taxes"].strip('$')

    drawer.set_form_data("name", full_name)
    drawer.set_form_data("street", street)
    drawer.set_form_data("city", city)
    drawer.set_form_data("area code", area_code)
    drawer.set_form_data("phone number", phone_number)
    drawer.set_form_data("date in", date_in)
    drawer.set_form_data("date out", date_out)
    drawer.set_form_data("total days", total_days)
    drawer.set_form_data("room rate", room_rate)
    drawer.set_form_data("room total", room_total)
    drawer.set_form_data("tax", room_taxes)
    drawer.save_image(full_name)
