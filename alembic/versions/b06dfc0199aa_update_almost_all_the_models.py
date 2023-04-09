"""update almost all the models

Revision ID: b06dfc0199aa
Revises: 95d36e9af56b
Create Date: 2023-04-09 12:24:57.243781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b06dfc0199aa'
down_revision = '95d36e9af56b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_phone', table_name='user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_user_phone', 'user', ['phone'], unique=False)
    # ### end Alembic commands ###
