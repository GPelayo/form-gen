from PIL import ImageDraw, Image, ImageFont
from configparser import ConfigParser
from re import findall
from datetime import datetime
import phonenumbers
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_CONFIG_DIR = os.path.join(APP_DIR, 'settings', 'font')
TEXT_OUTPUT_CONFIG_DIR = os.path.join(APP_DIR, 'settings', 'text_output')
FONT_FILES_DIR = os.path.join(APP_DIR, 'assets', 'fonts')
TEMPLATE_FILES_DIR = os.path.join(APP_DIR, 'assets', 'templates')

SOURCE_FIELD_NAME = 'source_field_name'

DEFAULT_IMAGE_FILE_TYPE = 'PNG'


class DocTemplateType:
    Image = 0


class AbstractFontFactory:
    file_path = None
    size = None

    def __init__(self, font_file, size):
        self.file_path = font_file
        self.size = size


class PillowImageFontFactory(AbstractFontFactory):
    def __init__(self, font_file, size):
        super().__init__(font_file, size)

    def create(self):
        return ImageFont.truetype(self.file_path, self.size)


class DocumentTemplate:
    font_factory = PillowImageFontFactory

    def __init__(self, template_name, file_ext="png"):
        self.name = template_name
        self.file_ext = file_ext
        self.template_path = os.path.join(TEMPLATE_FILES_DIR, "{}.{}".format(template_name, self.file_ext))
        self.text_output_dict = {}

        fnt_config = ConfigParser()
        fnt_config.read_file(open(os.path.join(FONT_CONFIG_DIR, "{}.ini".format(template_name)), 'r'))
        font_dict = {}
        for text_output_setting_name in fnt_config.sections():
            font_file_name = fnt_config.get(text_output_setting_name, 'font')
            font_size = fnt_config.getint(text_output_setting_name, 'size')
            font_file_path = os.path.join(FONT_FILES_DIR, font_file_name)
            font_dict[text_output_setting_name] = self.font_factory(font_file_path, font_size).create()

        txtout_cfg = ConfigParser()
        txtout_cfg.read_file(open(os.path.join(TEXT_OUTPUT_CONFIG_DIR, "{}.ini".format(template_name)), 'r'))
        for text_output_setting_name in txtout_cfg.sections():
            x = txtout_cfg.getint(text_output_setting_name, 'x')
            y = txtout_cfg.getint(text_output_setting_name, 'y')
            font_name = txtout_cfg.get(text_output_setting_name, 'font')
            font = font_dict[font_name]
            frm_data = TextOutputData(text_output_setting_name, x, y, font)
            frm_data.data_type = txtout_cfg.get(text_output_setting_name, 'data_type').lower()
            frm_data.source_type = txtout_cfg.get(text_output_setting_name, 'source_type', fallback="").lower()
            frm_data.source_field_name = txtout_cfg.get(text_output_setting_name, SOURCE_FIELD_NAME,
                                                        fallback="").lower()
            frm_data.phone_number_section = txtout_cfg.get(text_output_setting_name, 'phone_number_section',
                                                           fallback="").lower()
            frm_data.default_region_code = txtout_cfg.get(text_output_setting_name, 'default_region_code',
                                                          fallback="").upper()
            frm_data.source_region_code_key = txtout_cfg.get(text_output_setting_name, 'source_region_code_key',
                                                             fallback="").lower()
            frm_data.remove_char = txtout_cfg.get(text_output_setting_name, 'remove_char', fallback="").lower()
            self.text_output_dict[text_output_setting_name] = frm_data


class TextOutputData:
    def __init__(self, name, loc_x, loc_y, font, color="black"):
        self.__text = None
        self.name = name
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.font = font
        self.color = color
        self.data_type = None
        self.source_field_name = None
        self.phone_number_section = None
        self.default_region_code = None
        self.source_region_code_key = None
        self.remove_char = []

    def extract_text(self, data: dict):
        self.__text = str(self.__format_data(data))

    def __format_data(self, data):
        formatted_data = None
        if self.source_field_name:
            text_pattern = self.source_field_name
            if '[' in text_pattern and ']' in text_pattern:
                addends_vars = findall("\[[a-z\-_]+\]", text_pattern)
                if ':' in text_pattern:
                    method_name = findall(".*(?=:)", text_pattern)[0]
                    if method_name == 'subtract_days':
                        formatted_data = self.__subtract_days(data, addends_vars)
                else:
                    formatted_data = text_pattern
                    for var in addends_vars:
                        last_index = len(var)-1
                        text_sec = data[var[1:last_index]]
                        formatted_data = formatted_data.replace(var, text_sec)
            else:
                formatted_data = data[self.source_field_name]
        else:
            formatted_data = data[self.name]

        if self.data_type == 'phone_number':
            pn_pbj = phonenumbers.parse(formatted_data, self.default_region_code)
            if phonenumbers.is_valid_number_for_region(pn_pbj, self.default_region_code) and \
               (not data[self.source_region_code_key] or data[self.source_region_code_key] == self.default_region_code):
                    if self.phone_number_section == 'area code only':
                        formatted_data = str(pn_pbj.national_number)[:3]
                    elif self.phone_number_section == 'local number only':
                        formatted_data = str(pn_pbj.national_number)[3:]
            else:
                if self.phone_number_section == 'area code only':
                    formatted_data = ""
        for char in self.remove_char:
            formatted_data = formatted_data.replace(char, "")
        return formatted_data

    @staticmethod
    def __subtract_days(data, var_name_list, date_format="%m/%d/%Y"):
        date_var_late = var_name_list[0][1:len(var_name_list[0])-1]
        date_var_early = var_name_list[1][1:len(var_name_list[1]) - 1]
        diff_date = datetime.strptime(data[date_var_late], date_format) - datetime.strptime(data[date_var_early], date_format)
        return diff_date.days

    def get_text(self):
        return self.__text


class DocumentWriter:
    def __init__(self, template: DocumentTemplate):
        self.template = template

    def populate_form(self, data: dict):
        for output_name in self.template.text_output_dict.keys():
            self.template.text_output_dict[output_name].extract_text(data)

    def set_form_data(self, name, text):
        self.template.text_output_dict[name].text = text

    def save_image(self, file_location, open_preview=False):
        im = Image.open(self.template.template_path)
        draw = ImageDraw.Draw(im)
        self.__write_data(draw)
        file_sections = file_location.split(".")
        save_dir = os.path.dirname(file_location)
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        if len(file_sections) > 1:
            image_type = file_sections[1].upper()
            if image_type == "JPG":
                image_type = "JPEG"
            try:
                im.save(file_location, image_type)
            except KeyError:
                file_sections[1] = ".{}".format(DEFAULT_IMAGE_FILE_TYPE.lower())
                im.save("".join(file_sections), DEFAULT_IMAGE_FILE_TYPE)
        else:
            im.save("{}.{}".format(file_location, DEFAULT_IMAGE_FILE_TYPE.lower()))
        if open_preview:
            im.show()

    def __write_data(self, image_draw):
        for form_name in self.template.text_output_dict.keys():
            text_output_data = self.template.text_output_dict[form_name]
            if text_output_data:
                image_draw.text((text_output_data.loc_x, text_output_data.loc_y), text_output_data.get_text(),
                                font=text_output_data.font, fill=text_output_data.color)
