"""create table for exchange rates

Revision ID: 9fdaf56bb8e5
Revises: 9933b59d2c41
Create Date: 2018-08-12 20:31:36.339091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fdaf56bb8e5'
down_revision = '9933b59d2c41'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'exchange_rate',
        sa.Column("base_currency", sa.String(3)),
        sa.Column("other_currency", sa.String(3)),
        sa.Column("rate", sa.Float),
        sa.Column("date", sa.Date)
    )


def downgrade():
    op.drop_table('exchange_rate')