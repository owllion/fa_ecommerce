import uuid
from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import relationship

from ...database.db import Base
from ...utils.generate_id import gen_id


class CartItem(Base):
    __tablename__ = "cart_item"
    
    id = Column(String(80), primary_key=True, index=True,default= gen_id)

    cart_id = Column(String(80), ForeignKey("cart.id", ondelete="CASCADE"), nullable=False)

    parent_cart = relationship("Cart", back_populates="cart_items")

    product_id = Column(String(80), ForeignKey("product.id",ondelete="CASCADE"),nullable=False)

    quantity = Column(Integer, default=1)

    product = relationship("Product", backref="related_cart_item")

    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))