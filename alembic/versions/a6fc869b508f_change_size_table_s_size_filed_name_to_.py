"""change size table's size filed name to 'value' 

Revision ID: a6fc869b508f
Revises: 18cc74283f2a
Create Date: 2023-04-18 17:26:54.978948

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a6fc869b508f'
down_revision = '18cc74283f2a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('size', sa.Column('value', sa.String(length=5), nullable=False))
    op.drop_column('size', 'size')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('size', sa.Column('size', mysql.VARCHAR(length=5), nullable=False))
    op.drop_column('size', 'value')
    # ### end Alembic commands ###