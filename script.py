import argparse
import os
import time
from datetime import datetime

from config import config
from dbtables import repository
from fambudget import budgetparser

argparser = argparse.ArgumentParser()
argparser.add_argument("--fromdate", type=str, help="Process spending data, starting from this date (YYYY-MM-DD)")
argparser.add_argument("--filename", type=str, help="Full path of XLS file to parse from")
args = argparser.parse_args()

path = os.path.dirname(__file__)
filename = args.filename or (path + config['default_filename'])

parser = budgetparser.BudgetParser(filename, config)
repo = repository.Repository('sqlite:///data/data.sqlite', 'fambudget')
last_date = repo.get_latest_record_date()
if args.fromdate:
    fromdate = datetime.strptime(args.fromdate, '%Y-%m-%d').date()
    if last_date:
        if fromdate < last_date:
            last_date = fromdate
    else:
        last_date = fromdate

print('Parsing XLS file', filename, 'from date', last_date)
start = time.time()

repo.delete_data_since_date(last_date)
new_last_date = repo.fill_table_with_records(parser.process_next_record(last_date))
print('Parsing XLS file completed; last processed date is', new_last_date)
end = time.time()
print('Processing took', end - start, 'seconds')
