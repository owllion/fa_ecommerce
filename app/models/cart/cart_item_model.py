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


class CartItem(Base):
    __tablename__ = "cart_item"
    
    id = Column(String(36), primary_key=True, index=True,default=str(uuid.uuid4()))

    cart_id = Column(Integer, ForeignKey("cart.id", ondelete="CASCADE"), nullable=False)

    parent_cart = relationship("Cart", back_populates="cart_items")

    product_id = Column(Integer, ForeignKey("product.id",ondelete="CASCADE"),nullable=False)

    quantity = Column(Integer, default=1)

    product = relationship("Product", back_populates="cart_users")

    user = relationship("User", back_populates="cart_items")

    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))