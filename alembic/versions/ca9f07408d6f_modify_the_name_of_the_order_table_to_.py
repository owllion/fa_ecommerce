"""Modify the name of the 'order' table to avoid naming conflicts with MySQL.

Revision ID: ca9f07408d6f
Revises: c8b64ce740a8
Create Date: 2023-04-19 17:56:49.041660

"""
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op

# revision identifiers, used by Alembic.
revision = 'ca9f07408d6f'
down_revision = 'c8b64ce740a8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
   pass
