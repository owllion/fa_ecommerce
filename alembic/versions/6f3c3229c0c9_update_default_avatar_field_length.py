"""update default_avatar field length

Revision ID: 6f3c3229c0c9
Revises: 5c62fa1df720
Create Date: 2023-04-06 13:35:22.765218

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '6f3c3229c0c9'
down_revision = '5c62fa1df720'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('user', 'default_avatar', type_=sa.String(length=350))

def downgrade():
    op.alter_column('user', 'default_avatar', type_=sa.String(length=100))
