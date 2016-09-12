import csv
from formgen.data.api.wrappers import FormDataApi


class SampleCSVWrapper(FormDataApi):
    def __init__(self, file):
        if isinstance(file, str):
            self.file = open(file, 'r')
        else:
            self.file = file
        print(file)
        self.csv_reader = csv.DictReader(self.file)

    def __del__(self):
        if hasattr(self, 'file'):
            self.file.close()

    def retrieve_json(self):
        dummy_dict = [r for r in self.csv_reader]
        return dummy_dict
