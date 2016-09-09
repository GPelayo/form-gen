from data_pipeline.api import SampleFakeWrapper
from generator.writer import DocumentWriter, DocumentTemplate
import os

api = SampleFakeWrapper()
template = DocumentTemplate('sample', file_ext='png')
data = api.retrieve_json()

for gd in data:
    writer = DocumentWriter(template)
    writer.populate_form(gd)
    full_name = "{}.jpg".format(gd['name'])
    save_path = os.path.join('output_files', full_name)
    writer.save_image(save_path, open_preview=False)
