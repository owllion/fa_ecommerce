"""update order_model's paymentstatus default - again

Revision ID: baf4545603fb
Revises: 92e3123681c9
Create Date: 2023-04-21 19:31:58.481976

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'baf4545603fb'
down_revision = '92e3123681c9'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('order', 'payment_method',  default='credit_card')
    
    op.alter_column('order', 'payment_status',default='0')


def downgrade():
    op.alter_column('order', 'payment_status', existing_type=sa.Enum(0, 1, name='payment_status'), type_=sa.Integer(), existing_nullable=False, server_default='0')
    op.alter_column('order', 'payment_method', existing_type=sa.Enum('credit_card', 'line_pay', name='payment_methods'), type_=sa.String(length=20), existing_nullable=False, server_default='credit_card')
