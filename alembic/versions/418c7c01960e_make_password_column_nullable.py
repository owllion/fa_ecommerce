"""Make password column nullable

Revision ID: 418c7c01960e
Revises: ca9db515f6db
Create Date: 2023-04-25 15:47:25.087800

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '418c7c01960e'
down_revision = 'ca9db515f6db'
branch_labels = None
depends_on = None

def upgrade():
    # 將 password 欄位的現有類型作為第二個參數傳遞給 op.alter_column 方法
    op.alter_column('user', 'password', existing_type=sa.String(80), nullable=True)


def downgrade():
    op.alter_column('user', 'password', existing_type=sa.String(80), nullable=False)

