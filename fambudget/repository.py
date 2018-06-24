import sqlalchemy
from datetime import datetime

FACT_TABLE = "fambudget"


class Repository:
    def __init__(self, filename):
        self.engine = sqlalchemy.create_engine(filename)

        self.table = self.create_table(
            table_name=FACT_TABLE,
            fields=[
                ("spent_on", "date"),
                ("subject", "string"),
                ("category", "string"),
                ("subcount1", "string"),
                ("subcount2", "string"),
                ("amount", "integer"),
                ("currency", "string")
            ],
            create_id=True
        )

    def create_table_from_records(self, records):
        insert_command = self.table.insert()

        counter = 0
        for record in records:
            counter += 1
            if counter % 1000 == 0:
                print(counter, record)
            insert_command.execute(record)

    def create_table(self, table_name, fields,
                     create_id=False, schema=None):
        """Create a table with name `table_name` from a CSV file `file_name` with columns corresponding
        to `fields`. The `fields` is a list of two string tuples: (name, type) where type might be:
        ``integer``, ``float`` or ``string``.

        If `create_id` is ``True`` then a column with name ``id`` is created and will contain generated
        sequential record id.

        This is just small utility function for sandbox, play-around and testing purposes. It is not
        recommended to be used for serious CSV-to-table loadings. For more advanced CSV loadings use another
        framework, such as Brewery (http://databrewery.org).
        """

        # if table.exists():
        #   table.drop(checkfirst=False)
        metadata = sqlalchemy.MetaData(bind=self.engine)

        table = sqlalchemy.Table(table_name, metadata, autoload=False, schema=schema)
        if not table.exists():
            self.create_table(create_id, fields, table)

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

        if not table.exists():
            table.create()

        return table

    def get_latest_record_date(self):
        starting_date = self.engine \
            .execute(sqlalchemy.select([sqlalchemy.func.max(self.table.c.spent_on)])) \
            .fetchone()[0]

        return datetime.strptime(starting_date, '%Y-%m-%d').date()

    def delete_from_date(self, start_date):
        return self.engine \
            .execute(sqlalchemy.sql.expression.delete(self.table).where(self.table.c.spent_on >= start_date))
