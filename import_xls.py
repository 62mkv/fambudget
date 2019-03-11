# DONE: create a table for exchange rates
# DONE: implement import from xlsx
# DONE: update import fambudget to include also positive amounts
# DONE: create a table for multi-currency transactions (separate row per currency)
# 1) create table with columns: row_index, subject, category, subcount1, subcount2 (row_index is a primary key)
# 2) create table with columns: currency, amount, row_index
# DONE: create table for aggregated data
# 3) create table with columns: row_index, amount_rub, amount_eur
"""
Currently, script was used to populate data:

  insert into spendings (row_index, spent_on, subject, category, subcount1, subcount2)
  select distinct row_index, spent_on, subject, category, subcount1, subcount2 from fambudget

  insert into spending_amounts (row_index, amount, currency)
  select row_index, amount, currency from fambudget
"""
from config import config
from constants import RRU
# DONE: update model.json to support normalized tables (spendings/spending_amounts)
# DONE: update model.json: add cube for aggregated (multi-currency) table
# DONE: implement import from cbr API
from currency.importer import CurrencyRatesImporter

importer = CurrencyRatesImporter(config['database'], RRU)
importer.import_rates_from_xls("source-data/currency-rates/RC_F16_02_2019_T08_03_2019.xlsx")
