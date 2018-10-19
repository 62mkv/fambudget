"""create tables for multi-currency

Revision ID: b7c5f53675f8
Revises: 9fdaf56bb8e5
Create Date: 2018-10-19 20:28:29.477867

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b7c5f53675f8'
down_revision = '9fdaf56bb8e5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'spendings',
        sa.Column("row_index", sa.Integer, primary_key=True),
        sa.Column("category", sa.String(256)),
        sa.Column("spent_on", sa.Text),
        sa.Column("subject", sa.String(256)),
        sa.Column("subcount1", sa.String(256)),
        sa.Column("subcount2", sa.String(256))
    )

    op.create_table(
        'spending_amounts',
        sa.Column("amount", sa.Float),
        sa.Column("currency", sa.String(256)),
        sa.Column("row_index", sa.Integer)
    )

def downgrade():
    op.drop_table('spendings')
    op.drop_table('spending_amounts')
