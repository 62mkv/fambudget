from collections import namedtuple

import xlrd

from dbtables.structure import SpendingAmount, Spending

(
    SPENDING,
    INCOME,
    MOVEMENT
) = ('spending', 'income', 'movement')

SpendingWithAmounts = namedtuple('SpendingWithAmounts', ['spending', 'amounts'])

class BudgetParser:

    def __init__(self, filename, config):
        """
        Instantiates the BudgetParser instance

        :param filename: Path to XLS-file, from which data is imported
        :param config: dict with configuration (should have at least 'wallets' key and 'currency_sets' key),
            where 'wallets' value is a list of wallet titles; and 'currency_sets' value is a dict of currency IDs
        """
        self.book = xlrd.open_workbook(filename=filename)
        self.config = config
        self.sheet = self.book.sheet_by_name("Текущие")
        self.wallets = None
        self.__find_expense_columns()

    def __find_expense_columns(self):
        """
        Identifies which columns on the spreadsheet contain "wallets"-bound spending amount values

        :return: Dict with column number as key and a tuple of (currency, wallet_name) as value
        """
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

    def retrieve_spending_info(self, start_date=None):
        """
        Returns iterator, suitable for inserting into "spending/spending_amounts" tables

        Each item returned is a SpendingWithAmounts namedtuple
        """
        if self.wallets is None:
            raise ValueError('find_expense_columns must be called first!')

        row = 1
        while row < self.sheet.nrows - 1:
            row += 1
            spent_on = self.sheet.cell(row, 0).value
            try:
                if not spent_on:
                    continue

                # check to see if record date from file is less then start_date
                spent_on = xlrd.xldate.xldate_as_datetime(spent_on, 0).date()

                if start_date is not None and spent_on < start_date:
                    # skip this line, as we don't bother with records for dates earlier then "start_date"
                    continue

                values = [self.sheet.cell(row, col).value for col in range(1, 5)]

                spending = Spending(row, spent_on, *values)
                spending_with_amounts = SpendingWithAmounts(spending, [])

                for currency in self.config['currency_sets'].values():
                    names_and_cols = [(key, value[1]) for (key, value) in self.wallets.items() if value[0] == currency]
                    cols, names = zip(*names_and_cols)
                    values = [self.sheet.cell(row, col).value for col in cols]
                    amount = sum([float(x) for x in values if x], 0)

                    if amount < 0 or amount > 0:
                        amount_record = SpendingAmount(row, currency, amount)
                        spending_with_amounts.amounts.append(amount_record)

                yield spending_with_amounts

            except Exception as N:
                print(N, ' occurred at: ', row, values)

    def process_next_record(self, starting_date=None):
        """
        Returns iterator, suitable for bulk inserting into "fambudget" tables

        :param starting_date:
        :return:
        """
        names = ['row_index', 'spent_on', 'subject', 'category', 'subcount1', 'subcount2', 'currency', 'amount']
        for record in self.retrieve_spending_info(starting_date):
            for amount in record.amounts:
                result = dict(record.spending._asdict())
                result.update(dict(amount._asdict()))
                yield result
