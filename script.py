﻿import argparse
import os
import time
from datetime import datetime

from config import config
from fambudget import budgetparser
from fambudget.importer import FambudgetImporter, NormalizedImporter

DATABASE_FILE = config['database']

argparser = argparse.ArgumentParser()
argparser.add_argument("--fromdate", type=str, help="Process spending data, starting from this date (YYYY-MM-DD)")
argparser.add_argument("--filename", type=str, help="Full path of XLS file to parse from")
args = argparser.parse_args()

path = os.path.dirname(__file__)
filename = args.filename or (path + config['default_filename'])

parser = budgetparser.BudgetParser(filename, config)


def import_data(importer, title, iterator_retriever):
    last_date = importer.get_last_date()

    if args.fromdate:
        fromdate = datetime.strptime(args.fromdate, '%Y-%m-%d').date()
        if last_date:
            if fromdate < last_date:
                last_date = fromdate
        else:
            last_date = fromdate

    print('Parsing XLS file', filename, 'from date', last_date)
    start = time.time()

    importer.delete_data_since_date(last_date)

    new_last_date = importer.import_records_from_iterator(iterator_retriever(last_date))
    print('Parsing XLS file for ', title, 'completed; last processed date is', new_last_date)

    end = time.time()
    print('Processing took', end - start, 'seconds')


import_data(FambudgetImporter(DATABASE_FILE), "fambudget table", lambda x: parser.process_next_record(x))
import_data(NormalizedImporter(DATABASE_FILE), "normalized tables", lambda x: parser.retrieve_spending_info(x))
