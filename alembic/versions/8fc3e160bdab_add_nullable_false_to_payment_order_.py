"""add nullable=False to payment/order status and payment_method

Revision ID: 8fc3e160bdab
Revises: ca9f07408d6f
Create Date: 2023-04-19 18:03:58.232317

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8fc3e160bdab'
down_revision = 'ca9f07408d6f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order', 'order_status',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.alter_column('order', 'payment_method',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False)
    op.alter_column('order', 'payment_status',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.create_index(op.f('ix_order_id'), 'order', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_id'), table_name='order')
    op.alter_column('order', 'payment_status',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('order', 'payment_method',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True)
    op.alter_column('order', 'order_status',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
