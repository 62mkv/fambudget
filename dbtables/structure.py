from collections import namedtuple

SpendingAmount = namedtuple('SpendingAmount', ['row_index', 'currency', 'amount'])
Spending = namedtuple('Spending', ['row_index', 'spent_on', 'subject', 'category', 'subcount1', 'subcount2'])
Amount = namedtuple('Amount', ['row_index', 'currency', 'amount'])
