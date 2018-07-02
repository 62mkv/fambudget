import pathlib
from datetime import datetime
from unittest import TestCase

from fambudget.budgetparser import BudgetParser
from fambudget.budgetparser import RRU, EUR

(
    CARD_W,
    CARD_M,
    CASH,
    LOAN
) = ('Карта жены', 'Карта мужа', 'Наличные', 'Заем')

(
    SPENT_ON,
    SUBJECT,
    CATEGORY,
    SUBCOUNT1,
    SUBCOUNT2,
    AMOUNT,
    CURRENCY
) = ('spent_on', 'subject', 'category', 'subcount1', 'subcount2', 'amount', 'currency')

config = {
    'wallets': [CARD_W, CARD_M, CASH, LOAN],
    'currency_sets': {0: RRU, 1: EUR}
}


class TestBudgetParser(TestCase):
    def __init__(self, tests):
        path = pathlib.Path(__file__).parent / "test1.xls"
        filename = str(path)
        self.p = BudgetParser(filename, config)
        super().__init__(tests)

    def test_parser_initialization(self):
        expected = {
            5: (RRU, CARD_W),
            6: (RRU, CARD_M),
            7: (RRU, LOAN),
            8: (RRU, CASH),
            20: (EUR, CARD_W),
            21: (EUR, CARD_M),
            22: (EUR, LOAN),
            23: (EUR, CASH)
        }
        self.assertEqual(expected, self.p.wallets)

    def test_process_next_record(self):
        expected = [{AMOUNT: -2000.0,
                     CATEGORY: 'Обязательные платежи',
                     CURRENCY: 'RUB',
                     SPENT_ON: '2018-02-01',
                     SUBCOUNT1: 'Коммунальные',
                     SUBCOUNT2: '',
                     SUBJECT: 'Семья'},
                    {AMOUNT: -50.0,
                     CATEGORY: 'Обязательные платежи',
                     CURRENCY: 'EUR',
                     SPENT_ON: '2018-02-01',
                     SUBCOUNT1: 'Коммунальные',
                     SUBCOUNT2: '',
                     SUBJECT: 'Семья'},
                    {AMOUNT: -500.0,
                     CATEGORY: 'Обязательные платежи',
                     CURRENCY: 'RUB',
                     SPENT_ON: '2018-02-01',
                     SUBCOUNT1: 'Интернет',
                     SUBCOUNT2: '',
                     SUBJECT: 'Жена'},
                    {AMOUNT: -1000.0,
                     CATEGORY: 'Отдых',
                     CURRENCY: 'RUB',
                     SPENT_ON: '2018-02-02',
                     SUBCOUNT1: 'Алкоголь',
                     SUBCOUNT2: 'Пиво',
                     SUBJECT: 'Муж'},
                    {AMOUNT: -20.0,
                     CATEGORY: 'Отдых',
                     CURRENCY: 'EUR',
                     SPENT_ON: '2018-02-02',
                     SUBCOUNT1: 'Алкоголь',
                     SUBCOUNT2: 'Пиво',
                     SUBJECT: 'Муж'}
                    ]
        self.assertEqual(expected, list(self.p.process_next_record()))

    def test_process_next_record_with_offset(self):
        expected = [{AMOUNT: -1000.0,
                     CATEGORY: 'Отдых',
                     CURRENCY: 'RUB',
                     SPENT_ON: '2018-02-02',
                     SUBCOUNT1: 'Алкоголь',
                     SUBCOUNT2: 'Пиво',
                     SUBJECT: 'Муж'},
                    {AMOUNT: -20.0,
                     CATEGORY: 'Отдых',
                     CURRENCY: 'EUR',
                     SPENT_ON: '2018-02-02',
                     SUBCOUNT1: 'Алкоголь',
                     SUBCOUNT2: 'Пиво',
                     SUBJECT: 'Муж'}]
        self.assertEqual(expected, list(self.p.process_next_record(datetime.strptime('2018-02-02', '%Y-%m-%d').date())))
