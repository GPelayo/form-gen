import os
from formgen.generator.writer import AbstractImageTemplateFactory, TextOutputData, AbstractImageTemplate, \
    PillowImageFontFactory, FONT_FILES_DIR


class SampleUIImageTemplate(AbstractImageTemplate):
    def __init__(self, image_bytes, file_ext="png"):
        self.file_ext = file_ext
        self.image_data = image_bytes
        self.text_output_dict = {}


class SampleUITemplateFactory(AbstractImageTemplateFactory):
        name = 'django_input'

        def __init__(self, field_name):
            self.font_factory = PillowImageFontFactory()
            self.field_name = field_name

        def create(self):
            img_template = SampleUIImageTemplate(self.img_template)
            frm_data = TextOutputData(self.name,
                                      self.top_right_x, self.top_right_y,
                                      self.bottom_left_x, self.bottom_left_y,
                                      self.font, alignment=self.text_alignment, vert_alignment=self.vert_aligment)
            frm_data.source_field_name = self.field_name
            img_template.text_output_dict[self.name] = frm_data
            return img_template
