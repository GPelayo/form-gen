import zipfile
import os
from io import BytesIO, TextIOWrapper
from django.shortcuts import render
from django.http import HttpResponse
from sampleui.forms import ImageTemplateForm
from sampleapp.settings import TEMPLATES_FOLDER
from formgen.data.api import SampleCSVWrapper
from formgen.generator.writer import DocumentWriter, ImageTemplate


def main(request):
    template_filepath = os.path.join(TEMPLATES_FOLDER, 'main.html')
    if request.method == 'GET':
        form = ImageTemplateForm()
    else:
        form = ImageTemplateForm(request.POST)
        print('TEsttest')
        if form.is_valid():
            im_file = TextIOWrapper(request.FILES['csv_file'].file, request.encoding)
            data = SampleCSVWrapper(im_file).retrieve_json()

            template = ImageTemplate('sample', file_ext='png')
            gen_zip = BytesIO()
            zf = zipfile.ZipFile(gen_zip, 'a', zipfile.ZIP_DEFLATED, allowZip64=False)
            for gd in data:
                writer = DocumentWriter(template)
                writer.populate_form(gd)
                full_name = "{}.jpg".format(gd['name'])
                image_bytes = writer.get_image_file()
                zf.writestr(full_name, image_bytes)
            zf.close()
            with open('actual.zip', 'wb') as test:
                test.write(gen_zip.getvalue())
            res = HttpResponse(gen_zip.getvalue(), content_type="application/x-zip-compressed")
            res['Content-Disposition'] = "attachment; filename={}".format('gen.zip')
            res['Content-length'] = gen_zip.tell()
            return res
    data = {'form': form}
    return render(request, template_filepath, data)
