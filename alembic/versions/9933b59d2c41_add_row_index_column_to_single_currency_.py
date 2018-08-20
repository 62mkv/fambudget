"""add row_index column to single-currency table

Revision ID: 9933b59d2c41
Revises: 08a9721b683a
Create Date: 2018-07-04 20:57:41.809764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9933b59d2c41'
down_revision = '08a9721b683a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('fambudget',
                  sa.Column('row_index', sa.Integer)
                  )


def downgrade():
    op.drop_column('fambudget',
                   sa.Column('row_index', sa.Integer)
                   )
