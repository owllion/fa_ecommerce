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
)
from sqlalchemy.orm import relationship

from ..database.db import Base


class CartItem(Base):
    __tablename__ = "cart_item"
    
    product_id = Column(Integer, ForeignKey("product.id"))

    quantity = Column(Integer, default=1)

    product = relationship("Product", back_populates="cart_users")

    user = relationship("User", back_populates="cart_items")

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)