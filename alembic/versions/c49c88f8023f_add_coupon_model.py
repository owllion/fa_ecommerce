"""add Coupon model

Revision ID: c49c88f8023f
Revises: 755df036bf99
Create Date: 2023-04-10 00:04:47.087710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c49c88f8023f'
down_revision = '755df036bf99'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coupon',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('code', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('amount', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('expiry_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('minimum_amount', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('discount_type', sa.String(length=255), nullable=False),
    sa.Column('is_used', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_coupon_code'), 'coupon', ['code'], unique=False)
    op.create_index(op.f('ix_coupon_id'), 'coupon', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_coupon_id'), table_name='coupon')
    op.drop_index(op.f('ix_coupon_code'), table_name='coupon')
    op.drop_table('coupon')
    # ### end Alembic commands ###