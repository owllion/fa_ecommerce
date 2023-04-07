"""change avatar field length

Revision ID: 5c62fa1df720
Revises: 869d25acc277
Create Date: 2023-04-06 13:22:43.488149

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '5c62fa1df720'
down_revision = '869d25acc277'
branch_labels = None
depends_on = None



def upgrade():
    op.alter_column('user', 'upload_avatar', type_=sa.String(length=350))
    op.alter_column('user', 'default_avatar', type_=sa.String(length=350))

def downgrade():
    op.alter_column('user', 'upload_avatar', type_=sa.String(length=100))
    op.alter_column('user', 'default_avatar', type_=sa.String(length=100))