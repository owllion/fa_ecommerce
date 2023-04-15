"""add user_coupon and user_favorite

Revision ID: d78089304981
Revises: 0defae02884a
Create Date: 2023-04-14 12:39:41.736917

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd78089304981'
down_revision = '0defae02884a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('coupon_ibfk_1', 'coupon', type_='foreignkey')
    op.drop_column('coupon', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coupon', sa.Column('user_id', mysql.VARCHAR(length=80), nullable=False))
    op.create_foreign_key('coupon_ibfk_1', 'coupon', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###