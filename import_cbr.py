from datetime import date

from config import config
from constants import EUR
from currency.importer import CurrencyRatesImporter

importer = CurrencyRatesImporter(config['database'], EUR)
to_date = date(2019, 3, 12)
importer.import_rates_from_cbr(to_date)
