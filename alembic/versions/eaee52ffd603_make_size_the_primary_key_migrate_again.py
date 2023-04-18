"""Make size the primary key -migrate again

Revision ID: eaee52ffd603
Revises: e04e7791adc9
Create Date: 2023-04-16 16:28:29.004637

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'eaee52ffd603'
down_revision = 'e04e7791adc9'
branch_labels = None
depends_on = None

def upgrade():
    # op.execute("ALTER TABLE `cart_item` DROP FOREIGN KEY `cart_item_ibfk_1`;")
    # op.execute("ALTER TABLE `cart_item` DROP FOREIGN KEY `cart_item_ibfk_2`;")
    # op.execute("ALTER TABLE `cart_item` DROP PRIMARY KEY;")
    # op.execute("ALTER TABLE `cart_item` ADD CONSTRAINT `cart_item_ibfk_1` FOREIGN KEY (`cart_id`) REFERENCES `cart` (`id`) ON DELETE CASCADE;")
    # op.execute("ALTER TABLE `cart_item` ADD CONSTRAINT `cart_item_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE;")
    # op.execute("ALTER TABLE `cart_item` ADD PRIMARY KEY (`cart_id`, `product_id`, `size`);")
    # op.create_dummy_op()
    pass


def downgrade():
    pass
