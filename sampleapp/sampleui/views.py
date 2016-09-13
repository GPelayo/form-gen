import zipfile
import os
from io import BytesIO, TextIOWrapper
from django.shortcuts import render
from django.http import HttpResponse
from sampleui.forms import ImageTemplateForm
from sampleapp.settings import TEMPLATES_FOLDER
from formgen.data.api import SampleCSVWrapper
from formgen.generator.writer import DocumentWriter, ConfigImageTemplateFactory
from sampleui.formgenfactory import SampleUITemplateFactory


def main(request):
    template_filepath = os.path.join(TEMPLATES_FOLDER, 'main.html')
    if request.method == 'GET':
        form = ImageTemplateForm()
    else:
        form = ImageTemplateForm(request.POST)
        if form.is_valid():
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, request.encoding)
            tmplt_fctry = SampleUITemplateFactory(form.cleaned_data['target_field'])
            if 'template_image' in request.FILES:
                im_bytes = request.FILES['template_image'].read()
            else:
                im_bytes = ConfigImageTemplateFactory('sample').create().image_data
            tmplt_fctry.set_image(im_bytes)
            tmplt_fctry.set_text_area(form.cleaned_data['top_left_x'],
                                      form.cleaned_data['top_left_y'],
                                      form.cleaned_data['bottom_right_x'],
                                      form.cleaned_data['bottom_right_y'])
            tmplt_fctry.set_font(form.cleaned_data['font_type'], form.cleaned_data['font_size'])
            tmplt_fctry.set_alignment('center', 'middle')
            template = tmplt_fctry.create()
            data = SampleCSVWrapper(csv_file).retrieve_json()
            gen_zip = BytesIO()
            zf = zipfile.ZipFile(gen_zip, 'a', zipfile.ZIP_DEFLATED, allowZip64=False)
            for gd in data:
                writer = DocumentWriter(template)
                writer.populate_form(gd)
                full_name = "{}.jpg".format(gd['name'])
                csv_bytes = writer.get_image_file()
                zf.writestr(full_name, csv_bytes)
            zf.close()
            res = HttpResponse(gen_zip.getvalue(), content_type="application/x-zip-compressed")
            res['Content-Disposition'] = "attachment; filename={}".format('gen.zip')
            res['Content-length'] = gen_zip.tell()
            return res
    data = {'form': form}
    return render(request, template_filepath, data)
