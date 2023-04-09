import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import relationship

from ...database.db import Base


class OrderItem(Base):
    __tablename__ = 'order_item'

    id = Column(String(36), primary_key=True, index=True,default=str(uuid.uuid4()))

    order_id = Column(Integer,ForeignKey("order.id",ondelete="CASCADE"),nullable=False)

    parent_order = relationship("Order", back_populates="order_items")

    product_id = Column(Integer, ForeignKey("product.id",ondelete="CASCADE"),nullable=False)

    product = relationship("Product", backref="order_items")

    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))