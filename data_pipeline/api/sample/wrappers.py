from data_pipeline.api.sample import SAMPLE_DATA_DIR
from data_pipeline.api import FormDataApi
import csv
import os


class SampleFakeWrapper(FormDataApi):
    def __init__(self):
        with open(os.path.join(SAMPLE_DATA_DIR, 'dummy-data.csv'), 'r') as df:
            self.fieldnames = csv.DictReader(df).fieldnames

    def retrieve_json(self):
        with open(os.path.join(SAMPLE_DATA_DIR, 'dummy-data.csv'), 'r') as df:
            rdr = csv.DictReader(df)
            dummy_dict = [r for r in rdr]
        return dummy_dict
