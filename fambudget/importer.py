from dbtables.repository import SpendingsTable, SpendingAmountsTable


class NormalizedImporter:
    def __init__(self, dbfile):
        self.spendings_table = SpendingsTable(dbfile)
        self.spending_amounts_table = SpendingAmountsTable(dbfile)

    def get_last_date(self):
        return self.spendings_table.get_latest_record_date()

    def delete_data_since_date(self, start_date):
        row = self.spendings_table.get_least_row_index_for_date(start_date)
        self.spending_amounts_table.delete_data_since_row(row)
        self.spendings_table.delete_data_since_row(row)

    def import_records_from_iterator(self, iterator):
        last_processed_date = None
        for record in iterator:
            last_processed_date = record.spending.spent_on
            self.spendings_table.insert_record(dict(record.spending._asdict()))
            for amount in record.amounts:
                self.spending_amounts_table.insert_record(dict(amount._asdict()))
        return last_processed_date
