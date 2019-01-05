"""create_more_correct_multi_currency_table

Revision ID: 06945e551cd7
Revises: b2ca0cde5152
Create Date: 2019-01-05 21:12:49.025223

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '06945e551cd7'
down_revision = 'b2ca0cde5152'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'spending_amount_multi_currency',
        sa.Column("amount", sa.Float),
        sa.Column("currency", sa.String(256)),
        sa.Column("row_index", sa.Integer)
    )


def downgrade():
    op.drop_table('spending_amount_multi_currency')
