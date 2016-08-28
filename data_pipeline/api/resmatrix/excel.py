import os
import xlwt

DEFAULT_FILE_NAME = "booking-data.xls"
EXCEL_FOLDER = "excel-files"


class ResBookingBuilder:
    data = None
    filename = None
    missing_data_logger = None
    header_names = None

    def __init__(self, filename=DEFAULT_FILE_NAME):
        self.data = []
        self.filename = filename

    def set_header_names(self, headers):
        self.header_names = headers

    def add(self, row):
        self.data.append(row)
        # for table_field in self.table_fields:
        #     cells = driver.find_elements_by_css_selector()
        #     cell_str = ", ".join([cell.text.replace("/n", "") for cell in cells])
        #     self.data.append((table_field[1], cell_str))

    def write_file(self):
        #TODO Add file lock
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Bookings")
        row_num = 0

        header_font = xlwt.XFStyle()
        header_font.font.bold = True

        for field_index in range(len(self.header_names)):
            title = self.header_names[field_index]
            ws.write(row_num, field_index, title, header_font)

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1
        for row in self.data:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        if not os.path.exists(EXCEL_FOLDER):
            os.mkdir(EXCEL_FOLDER)

        file_path = os.path.join(EXCEL_FOLDER, self.filename)

        wb.save(file_path)

