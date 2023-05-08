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

    cart_id = Column(
        String(80), ForeignKey("cart.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )

    parent_cart = relationship("Cart", back_populates="cart_items")

    product_id = Column(
        String(80), ForeignKey("product.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )

    product = relationship("Product", back_populates="related_cart_item")

    size = Column(String(5), primary_key=True, nullable=False)

    qty = Column(Integer, default=1)

    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
