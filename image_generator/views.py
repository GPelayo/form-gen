from django.shortcuts import render
from generator import TEMPLATES_FOLDER
import os


def main(request):
    template_filepath = os.path.join(TEMPLATES_FOLDER, 'main.html')
    return render(request, template_filepath)
