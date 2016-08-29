from generator.writer import DocumentTemplate, DocumentWriter
from data_pipeline.api.resmatrix.gaddery import ResMatrixBookingGaddery
import os
import json

booking_date = "8/26/16"
end_date = "8/26/16"

gd = ResMatrixBookingGaddery(booking_date, end_date)
data = gd.get_scraped_data()

with open('itr.json', 'w+') as test_file:
    json.dump(data, test_file)

with open('itr.json', 'r') as test_file:
    data = json.load(test_file)

template = DocumentTemplate('sample')

for gd in data:
    writer = DocumentWriter(template)
    writer.populate_form(gd)
    full_name = "{} {}.mov".format(gd["first_name"], gd["last_name"])
    save_path = os.path.join('output_files', full_name)
    writer.save_image(save_path, open_preview=True)
