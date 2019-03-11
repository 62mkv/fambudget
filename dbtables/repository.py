import sqlalchemy
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import select

from constants import MULTI_CURRENCY, EXCHANGE_RATE, SPENDINGS, SPENDING_AMOUNTS

SPENDING_AMOUNTS_SCHEMA = [
    ("row_index", "integer"),
    ("currency", "string"),
    ("amount", "float"),
]

SCHEMA = {
    MULTI_CURRENCY: SPENDING_AMOUNTS_SCHEMA,
    EXCHANGE_RATE: [
        ("base_currency", "string"),
        ("other_currency", "string"),
        ("rate", "float"),
        ("date", "date")
    ],
    SPENDINGS: [
        ("row_index", "integer"),
        ("spent_on", "date"),
        ("subject", "string"),
        ("category", "string"),
        ("subcount1", "string"),
        ("subcount2", "string"),
    ],
    SPENDING_AMOUNTS: SPENDING_AMOUNTS_SCHEMA
}


def create_table(engine, table_name, fields, create_id=False, schema=None):
    """
    Create SQLAlchemy table according to provided schema
    """
    metadata = sqlalchemy.MetaData(bind=engine)
    table = sqlalchemy.Table(table_name, metadata, autoload=False, schema=schema)
    type_map = {"integer": sqlalchemy.Integer,
                "float": sqlalchemy.Numeric,
                "string": sqlalchemy.String(256),
                "text": sqlalchemy.Text,
                "date": sqlalchemy.Date,
                "boolean": sqlalchemy.Integer}

    if create_id:
        col = sqlalchemy.schema.Column('id', sqlalchemy.Integer, primary_key=True)
        table.append_column(col)

    field_names = []

    for (field_name, field_type) in fields:
        col = sqlalchemy.schema.Column(field_name, type_map[field_type.lower()])
        table.append_column(col)
        field_names.append(field_name)

    return table


class Repository:
    def __init__(self, filename, tablename):
        self.engine = sqlalchemy.create_engine(filename, echo=False)
        self.table = create_table(
            engine=self.engine,
            table_name=tablename,
            fields=SCHEMA[tablename],
            create_id=False,
        )
        self.insert_command = self.table.insert()

    def insert_record(self, record):
        self.insert_command.execute(record)


class RowIndexTable(Repository):
    def __init__(self, filename, tablename):
        if (dict(SCHEMA[tablename]).get("row_index") is None):
            raise AttributeError("This table has no row_index attribute")
        super().__init__(filename, tablename)

    def delete_data_since_row(self, start_row):
        if start_row:
            self.engine \
                .execute(sqlalchemy.sql.expression.delete(self.table).where(self.table.c.row_index >= start_row))

    def get_last_row_index(self):
        return self.engine \
            .execute(sqlalchemy.select([sqlalchemy.func.max(self.table.c.row_index)])) \
            .fetchone()[0]

    def get_records_with_row_index(self, row):
        return self.engine.execute(sqlalchemy.select(self.table.columns).where(self.table.c.row_index == row))


class TableWithDateField(Repository):
    def __init__(self, filename, tablename, date_column='spent_on'):
        super().__init__(filename, tablename)
        self.date_column_name = date_column

    def fill_table_with_records(self, records):
        processed_date = None

        counter = 0
        for record in records:
            self.insert_record(record)
            counter += 1
            if counter % 1000 == 0:
                print(counter, record)
            processed_date = record[self.date_column_name]

        return processed_date

    def get_latest_record_date(self):
        last_date = self.engine \
            .execute(sqlalchemy.select([sqlalchemy.func.max(self.table.c[self.date_column_name])])) \
            .fetchone()[0]

        return last_date

    def delete_data_since_date(self, start_date):
        if start_date:
            self.engine \
                .execute(sqlalchemy.sql.expression.delete(self.table).where(self.table.c.spent_on >= start_date))


class SpendingsTable(RowIndexTable, TableWithDateField):
    def __init__(self, filename):
        super(RowIndexTable, self).__init__(filename, SPENDINGS)
        super(TableWithDateField, self).__init__(filename, SPENDINGS)

    def get_least_row_index_for_date(self, date):
        if date:
            conn = self.engine.connect()
            stmt = select([func.min(self.table.c.row_index)]).where(self.table.c.spent_on >= date)
            return conn.execute(stmt).scalar()


class SpendingAmountsTable(RowIndexTable):
    def __init__(self, filename):
        super().__init__(filename, SPENDING_AMOUNTS)


class SpendingMultiCurrencyAmounts(RowIndexTable):
    def __init__(self, filename):
        super().__init__(filename, MULTI_CURRENCY)


class CurrencyRates(TableWithDateField):
    def __init__(self, filename):
        super().__init__(filename, EXCHANGE_RATE, 'date')

    def get_rate_for_date(self, currency_from, currency_to, date):
        return float(self.engine.execute(sqlalchemy.select([self.table.c.rate])
                                         .where((self.table.c[self.date_column_name] == date)
                                                & (self.table.c.base_currency == currency_from)
                                                & (self.table.c.other_currency == currency_to)
                                                )).fetchone()[0])
