"""change cart_item's quantity to qty

Revision ID: 8b3b4036c1e2
Revises: eaee52ffd603
Create Date: 2023-04-17 00:22:28.040793

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8b3b4036c1e2'
down_revision = 'eaee52ffd603'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart_item', sa.Column('qtys', sa.Integer(), nullable=True))
    op.drop_column('cart_item', 'quantity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart_item', sa.Column('quantity', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('cart_item', 'qtys')
    # ### end Alembic commands ###
