import os
from django import forms
from formgen.generator.writer import FONT_FILES_DIR


class ImageTemplateForm(forms.Form):
    font_names = [(fn.split('.')[0].title(), fn.split('.')[0].title()) for fn in os.listdir(FONT_FILES_DIR)]
    template_image = forms.ImageField(required=False)
    font_type = forms.ChoiceField(choices=font_names)
    font_size = forms.IntegerField()
    csv_file = forms.FileField(required=False)
    target_field = forms.CharField(max_length=35)
    top_left_x = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    top_left_y = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    bottom_right_x = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    bottom_right_y = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
