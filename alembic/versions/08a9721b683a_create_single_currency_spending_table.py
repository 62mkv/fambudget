"""create single-currency spending table

Revision ID: 08a9721b683a
Revises: 
Create Date: 2018-07-04 19:11:44.408857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08a9721b683a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'fambudget',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column("amount", sa.Float),
        sa.Column("category", sa.String(256)),
        sa.Column("currency", sa.String(256)),
        sa.Column("spent_on", sa.Text),
        sa.Column("subject", sa.String(256)),
        sa.Column("subcount1", sa.String(256)),
        sa.Column("subcount2", sa.String(256))
    )


def downgrade():
    op.drop_table('fambudget')
