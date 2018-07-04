import xlrd

(
    SPENDING,
    INCOME,
    MOVEMENT
) = ('spending', 'income', 'movement')

(RRU, EUR) = ('RUB', 'EUR')


class BudgetParser:

    def __init__(self, filename, config):
        self.book = xlrd.open_workbook(filename=filename)
        self.config = config
        self.sheet = self.book.sheet_by_name("Текущие")
        self.wallets = None
        self.__find_expense_columns()

    def __find_expense_columns(self):
        if self.wallets is not None:
            return self.wallets

        wallets = self.config['wallets']
        currencies = self.config['currency_sets']
        current_set = dict()
        result = dict()
        current_index = 0
        for col in range(self.sheet.ncols):
            v = self.sheet.cell(0, col).value
            if v in wallets:
                if v in current_set.values():
                    for (column, wallet) in current_set.items():
                        result[column] = (currencies[current_index], wallet)
                    current_set = dict()
                    current_index += 1
                current_set[col] = v

        if len(current_set) > 0:
            for (column, wallet) in current_set.items():
                result[column] = (currencies[current_index], wallet)

        self.wallets = result

    def process_next_record(self, starting_date=None):

        if self.wallets is None:
            raise ValueError('find_expense_columns must be called first!')

        row = 1
        while row < self.sheet.nrows - 1:
            row += 1
            spent_on = self.sheet.cell(row, 0).value
            try:
                if not spent_on:
                    continue

                # check to see if date from file is less then starting_date
                spent_on = xlrd.xldate.xldate_as_datetime(spent_on, 0).date()

                if starting_date is not None and spent_on < starting_date:
                    continue

                names = ('subject', 'category', 'subcount1', 'subcount2')
                values = [self.sheet.cell(row, col).value for col in range(1, 5)]

                record = dict(zip(names, values))
                record['spent_on'] = spent_on.isoformat()

                for currency in self.config['currency_sets'].values():
                    names_and_cols = [(key, value[1]) for (key, value) in self.wallets.items() if value[0] == currency]
                    cols, names = zip(*names_and_cols)
                    values = [self.sheet.cell(row, col).value for col in cols]
                    amount = sum([float(x) for x in values if x], 0)

                    if amount < 0:
                        spending = dict()
                        spending.update(record)
                        spending['currency'] = currency
                        spending['amount'] = amount
                        spending['row_index'] = row
                        yield spending
            except Exception as N:
                print(N, ' occurred at: ', row, values)
