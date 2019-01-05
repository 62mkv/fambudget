(RRU, EUR) = ('RUB', 'EUR')

# this table needs to be deprecated - it contains one spending record per currency
SINGLE_CURRENCY = 'fambudget'

# this is a helper table that stores currency exchange rates
EXCHANGE_RATE = 'exchange_rate'

# this table stores spending records as such (date, subject, item, but not amounts)
SPENDINGS = 'spendings'

# this table stores amounts of spendings in 'native' currencies (multiple records per spending)
SPENDING_AMOUNTS = 'spending_amounts'

# this table stores amounts of spendings, aggregated in each of the currencies (one record per spending per currency)
MULTI_CURRENCY = 'spending_amount_multi_currency'
