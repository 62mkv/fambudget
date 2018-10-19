"""create table for aggregated accounting in multiple currencies

Revision ID: b2ca0cde5152
Revises: b7c5f53675f8
Create Date: 2018-10-19 20:37:49.714101

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b2ca0cde5152'
down_revision = 'b7c5f53675f8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'agg_multi_currency',
        sa.Column("row_index", sa.Integer, primary_key=True),
        sa.Column("amount_eur", sa.Float),
        sa.Column("amount_rub", sa.Float)
    )

def downgrade():
    op.drop_table('agg_multi_currency')
