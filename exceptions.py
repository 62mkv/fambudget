class SpendingRowNotFound(Exception):
    pass


class NoMoreCurrencyRates(Exception):
    def __init__(self, currency_from, currency_to, date):
        super().__init__("No rate found for conversion %s:%s for date %s" % (currency_from, currency_to, date))


class UnknownCurrency(Exception):
    pass
