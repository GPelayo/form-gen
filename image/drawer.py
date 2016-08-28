from PIL import ImageDraw, Image, ImageFont
from configparser import ConfigParser
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_CONFIG_DIR = os.path.join(APP_DIR, 'settings', 'font')
TEXT_OUTPUT_CONFIG_DIR = os.path.join(APP_DIR, 'settings', 'text_output')
FONT_FILES_DIR = os.path.join(APP_DIR, 'assets', 'fonts')
TEMPLATE_FILES_DIR = os.path.join(APP_DIR, 'assets', 'templates')


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

        text_output = ConfigParser()
        text_output.read_file(open(os.path.join(TEXT_OUTPUT_CONFIG_DIR, "{}.ini".format(template_name)), 'r'))
        for text_output_setting_name in text_output.sections():
            x = text_output.getint(text_output_setting_name, 'x')
            y = text_output.getint(text_output_setting_name, 'y')
            font_name = text_output.get(text_output_setting_name, 'font')
            font = font_dict[font_name]
            self.text_output_dict[text_output_setting_name] = FormData(x, y, font)


class FormData:
    def __init__(self, loc_x, loc_y, font, color="black"):
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.font = font
        self.text = None
        self.color = color


class DocumentDrawer:
    def __init__(self, template: DocumentTemplate):
        self.template = template

    def set_form_data(self, name, text):
        self.template.text_output_dict[name].text = text

    def save_image(self, file_location, open_preview=False):
        im = Image.open(self.template.template_path)
        draw = ImageDraw.Draw(im)
        self.__write_data(draw)
        with open("{}.{}".format(file_location, self.template.file_ext), 'w+b') as image_file:
            im.save(image_file, 'PNG')

        if open_preview:
            im.show()

    def __write_data(self, image_draw):
        for form_name in self.template.text_output_dict.keys():
            form_data = self.template.text_output_dict[form_name]
            if form_data.text:
                image_draw.text((form_data.loc_x, form_data.loc_y), form_data.text, font=form_data.font,
                                fill=form_data.color)
