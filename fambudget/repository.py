from datetime import datetime

import sqlalchemy

from fambudget.budgetparser import EUR, RRU

ONE_CURRENCY = "fambudget"
ALL_CURRENCY = "fambudget_ac"

SCHEMA = {
    ONE_CURRENCY: [
        ("amount", "float"),
        ("category", "string"),
        ("currency", "string"),
        ("row_index", "integer"),
        ("spent_on", "date"),
        ("subject", "string"),
        ("subcount1", "string"),
        ("subcount2", "string")
    ],
    ALL_CURRENCY: [
        ("amount_" + EUR, "float"),
        ("amount_" + RRU, "float"),
        ("category", "string"),
        ("spent_on", "date"),
        ("subject", "string"),
        ("subcount1", "string"),
        ("subcount2", "string")
    ]
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
                "date": sqlalchemy.Text,
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
        self.engine = sqlalchemy.create_engine(filename)

        self.table = create_table(
            engine=self.engine,
            table_name=tablename,
            fields=SCHEMA[tablename],
            create_id=True
        )

    def fill_table_with_records(self, records):
        insert_command = self.table.insert()

        counter = 0
        for record in records:
            counter += 1
            if counter % 1000 == 0:
                print(counter, record)
            insert_command.execute(record)
            processed_date = record['spent_on']

        return processed_date

    def get_latest_record_date(self):
        starting_date = self.engine \
            .execute(sqlalchemy.select([sqlalchemy.func.max(self.table.c.spent_on)])) \
            .fetchone()[0]

        return datetime.strptime(starting_date, '%Y-%m-%d').date() if starting_date else None

    def delete_from_date(self, start_date):
        if start_date:
            self.engine \
                .execute(sqlalchemy.sql.expression.delete(self.table).where(self.table.c.spent_on >= start_date))
