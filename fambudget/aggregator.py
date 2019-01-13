from config import config
from constants import RRU
from dbtables.repository import SpendingAmountsTable, SpendingMultiCurrencyAmounts, SpendingsTable, CurrencyRates
from dbtables.structure import SpendingAmount, Spending
from .exceptions import SpendingRowNotFound


class Aggregator:
    def __init__(self, filename):
        self.spending_amounts = SpendingAmountsTable(filename)
        self.spending_multi_currency_amounts = SpendingMultiCurrencyAmounts(filename)
        self.spendings = SpendingsTable(filename)
        self.rates = CurrencyRates(filename)
        self.currencies = config['currency_sets'].values()

    def aggregate_spendings(self):
        """
        Fills the table of aggregated spendings by scanning the spendings/spending_amounts tables

        :return: None
        """

        # TODO: create a procedure to fill aggregated table

        # calculate last row_index of the aggregated table
        agg_last = self.agg_calculate_last_row()
        # calculate last row_index in spendings
        spending_last = self.spendings_calculate_last_row()

        # delete row for this row_index from the aggregated table (only makes sense for the first one)
        self.spending_multi_currency_amounts.delete_data_since_row(agg_last)

        # determine rows one needs to convert (every row from last one in the aggregated
        # table to the last one in spendings)

        # for each row_index,
        for row_index in range(agg_last, spending_last):
            try:
                if (row_index % 100 == 0):
                    print("Processing row ", row_index)
                spent_on = self.get_date_for_row(row_index)
                # initialize 0 records for each currency
                multi_currency_dict = dict(zip(self.currencies, (0,) * len(self.currencies)))

                #     take all rub amounts, save as rub + convert to eur
                #     take all eur amounts, add to eur saved + convert to rub and add to rub saved
                for spending in self.spending_amounts.get_records_with_row_index(row_index):
                    spending_record = SpendingAmount(spending[0], spending[1], float(spending[2]))
                    for currency in self.currencies:
                        multi_currency_dict[currency] += self.convert(spending_record.currency, currency,
                                                                      spending_record.amount,
                                                                      spent_on)
                #     insert record into aggregated table
                for currency in self.currencies:
                    amount = multi_currency_dict[currency]
                    if amount > 0 or amount < 0:
                        record = SpendingAmount(row_index, currency, amount)
                        self.spending_multi_currency_amounts.insert_record(record._asdict())
            except SpendingRowNotFound:
                pass

    def agg_calculate_last_row(self):
        return self.spending_multi_currency_amounts.get_last_row_index() or 2

    def spendings_calculate_last_row(self):
        return self.spending_amounts.get_last_row_index() or 2

    def convert(self, currency_from, currency_to, amount, date):
        if currency_from == currency_to:
            return amount
        else:
            exchange_rate = self.get_exchange_rate_for_date(currency_from, currency_to, date)
            return float(amount) / float(exchange_rate)

    # TODO: provide implementation
    def get_date_for_row(self, row_index):
        record = self.spendings.get_records_with_row_index(row_index).fetchone()
        if record is None:
            raise SpendingRowNotFound
        spending = Spending(*record)
        return spending.spent_on

    # TODO: provide implementation
    def get_exchange_rate_for_date(self, currency_from, currency_to, date):
        if currency_from == RRU:
            rate = self.rates.get_rate_for_date(currency_from, currency_to, date)
        else:
            rate = 1 / self.rates.get_rate_for_date(currency_to, currency_from, date)
        # print(currency_from, currency_to, date, rate)
        return rate
