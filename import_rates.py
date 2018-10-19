# DONE: create a table for exchange rates
# DONE: implement import from xlsx
# DONE: update import fambudget to include also positive amounts
# TODO: create a table for multi-currency transactions (separate row per currency)
# TODO: create a procedure to fill multi-currency table
# TODO: update mappings.json in order to be able to build cubes for multi-currency table
# TODO: implement import from cbr API
from datetime import timedelta

from openpyxl.reader import excel

from constants import EUR, RRU
from dbtables import repository


def read_values(filename):
    wb = excel.load_workbook(filename=filename)

    ws = wb.worksheets[0]

    row = 2

    current_date = ws.cell(row, 2).value
    current_rate = ws.cell(row, 3).value

    while ws.cell(row, 1).value is not None:
        next_date = ws.cell(row, 2).value
        while next_date > current_date:
            names = ('base_currency', 'other_currency', 'rate', 'date')
            values = ( RRU, EUR, current_rate, current_date)
            record = dict(zip(names, values))
            yield record
            current_date += timedelta(days=1)

        current_rate = ws.cell(row, 3).value
        row += 1


table = repository.Repository('sqlite:///data/data.sqlite', 'exchange_rate')
table.fill_table_with_records(read_values("source-data/RC_F01_01_2008_T05_07_2018.xlsx"), date_field_name='date')