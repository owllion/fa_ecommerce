"""update user phone's length

Revision ID: 024de0eba2ea
Revises: 2110cd356179
Create Date: 2023-04-14 14:25:31.831539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '024de0eba2ea'
down_revision = '2110cd356179'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite_item',
    sa.Column('user_id', sa.String(length=80), nullable=False),
    sa.Column('product_id', sa.String(length=80), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'product_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite_item')
    # ### end Alembic commands ###