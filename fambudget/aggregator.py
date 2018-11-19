from constants import MULTI_CURRENCY, SPENDINGS
from dbtables.repository import RowIndexTable

AGG_TABLE = RowIndexTable(MULTI_CURRENCY)
SPENGINGS_TABLE = RowIndexTable(SPENDINGS)

def agg_calculate_last_row():
    return AGG_TABLE.get_last_row_index()

def spendings_calculate_last_row():
    return SPENGINGS_TABLE.get_last_row_index()

def aggregate_spendings():
    """
    Fills the table of aggregated spendings by scanning the spendings/spending_amounts tables

    :return: None
    """

# TODO: create a procedure to fill aggregated table
# calculate last row_index of the aggregated table
# calculate last row_index in spendings
# determine rows one needs to convert (every row from last one in the aggregated table to the last one in spendings)
# for each row_index,
#     delete row for this row_index from the aggregated table (only makes sense for the first one)
#     take all rub amounts, save as rub + convert to eur
#     take all eur amounts, add to eur saved + convert to rub and add to rub saved
#     insert record into aggregated table
    agg_last = agg_calculate_last_row()
    spending_last = spendings_calculate_last_row()

    # delete last record from aggregated as it could have been updated
    agg_drop_record(agg_last)

    for row_index in range(agg_last, spending_last):
        agg_add_record(calculate_agg_record(row_index))