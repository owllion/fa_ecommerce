"""update user model

Revision ID: 95d36e9af56b
Revises: 6f3c3229c0c9
Create Date: 2023-04-06 17:24:01.141761

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '95d36e9af56b'
down_revision = '6f3c3229c0c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.String(length=30), nullable=True))
    op.add_column('user', sa.Column('last_name', sa.String(length=30), nullable=True))
    op.add_column('user', sa.Column('phone', sa.String(length=15), nullable=True))
    op.drop_index('ix_user_username', table_name='user')
    op.create_index(op.f('ix_user_first_name'), 'user', ['first_name'], unique=False)
    op.create_index(op.f('ix_user_last_name'), 'user', ['last_name'], unique=False)
    op.create_index(op.f('ix_user_phone'), 'user', ['phone'], unique=False)
    op.drop_column('user', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', mysql.VARCHAR(length=30), nullable=True))
    op.drop_index(op.f('ix_user_phone'), table_name='user')
    op.drop_index(op.f('ix_user_last_name'), table_name='user')
    op.drop_index(op.f('ix_user_first_name'), table_name='user')
    op.create_index('ix_user_username', 'user', ['username'], unique=False)
    op.drop_column('user', 'phone')
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###
