import logging

from config import config
from constants import RRU
from currency.importer import CurrencyRatesImporter
from dbtables.repository import SpendingAmountsTable, SpendingMultiCurrencyAmounts, SpendingsTable, CurrencyRates
from dbtables.structure import SpendingAmount, Spending
from exceptions import SpendingRowNotFound


class Aggregator:
    def __init__(self, filename):
        self.spending_amounts = SpendingAmountsTable(filename)
        self.spending_multi_currency_amounts = SpendingMultiCurrencyAmounts(filename)
        self.spendings = SpendingsTable(filename)
        self.rates = CurrencyRates(filename)
        self.currencies = config['currency_sets'].values()
        self.currency_importers = [
            CurrencyRatesImporter(filename, c) for c in self.currencies if c != RRU
        ]

    def update_rates(self, till_date):
        logging.info('Updating currency rates till %s', till_date)
        for currency_importer in self.currency_importers:
            logging.info('Calling read rates for %s', currency_importer.other_currency)
            currency_importer.import_rates_from_cbr(till_date)

    def aggregate_spendings_since_date(self, last_date):
        """
        Fills the table of aggregated spendings by scanning the spendings/spending_amounts tables

        :return: None
        """
        # delete rows since last_date
        row_for_last_date = self.spendings.get_least_row_index_for_date(last_date)
        self.spending_multi_currency_amounts.delete_data_since_row(row_for_last_date)

        # calculate last row_index of the aggregated table
        last_aggregated_row = self.agg_calculate_last_row()
        logging.info('Last aggregated row is %s', self.get_date_for_row(last_aggregated_row))

        # calculate last row_index in spendings
        last_spendings_row = self.spendings_calculate_last_row()
        last_spendings_date = self.get_date_for_row(last_spendings_row)
        logging.info('Aggregating spendings till %s', last_spendings_date)

        # delete row for this row_index from the aggregated table (only makes sense for the first one)
        self.spending_multi_currency_amounts.delete_data_since_row(last_aggregated_row)

        # determine rows one needs to convert (every row from last one in the aggregated
        # table to the last one in spendings)

        self.update_rates(last_spendings_date)
        # for each row_index,
        for row_index in range(last_aggregated_row, last_spendings_row + 1):
            try:
                if row_index % 100 == 0:
                    logging.debug('Processing row %d', row_index)
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

    def get_date_for_row(self, row_index):
        record = self.spendings.get_records_with_row_index(row_index).fetchone()
        if record is None:
            raise SpendingRowNotFound
        spending = Spending(*record)
        return spending.spent_on

    def get_exchange_rate_for_date(self, currency_from, currency_to, date):
        if currency_from == RRU:
            rate = self.rates.get_rate_for_date(currency_from, currency_to, date)
        else:
            rate = 1 / self.rates.get_rate_for_date(currency_to, currency_from, date)
        return rate
