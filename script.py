import argparse
import os
from datetime import datetime

from config import config
from fambudget import budgetparser, repository

argparser = argparse.ArgumentParser()
argparser.add_argument("--fromdate", type=str, help="Process spending data, starting from this date (YYYY-MM-DD)")
argparser.add_argument("--filename", type=str, help="Full path of XLS file to parse from")
args = argparser.parse_args()

path = os.path.dirname(__file__)
filename = args.filename or (path + "test2.xls")

parser = budgetparser.BudgetParser(filename, config)
repo = repository.Repository('sqlite:///data.sqlite')
last_date = repo.get_latest_record_date()
if args.fromdate:
    fromdate = datetime.strptime(args.fromdate, '%Y-%m-%d').date()
    if last_date:
        if fromdate < last_date:
            last_date = fromdate
    else:
        last_date = fromdate

print('Parsing XLS file', filename, 'from date', last_date)
repo.delete_from_date(last_date)
new_last_date = repo.create_table_from_records(parser.process_next_record(last_date))
print('Parsing XLS file completed; last processed date is', new_last_date)