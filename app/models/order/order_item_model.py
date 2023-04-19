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
from ...utils.generate_id import gen_id


class OrderItem(Base):
    __tablename__ = 'order_item'

    order_id = Column(
        String(80),
        ForeignKey("order.id",ondelete="CASCADE"),
        primary_key= True,
        nullable=False
    )

    product_id = Column(
        String(80), 
        ForeignKey("product.id",ondelete="CASCADE"),
        primary_key= True,
        nullable=False
    )

    parent_order = relationship(
        "Order", 
        back_populates="order_items"
    )

    product_info = relationship(
        "Product", 
        backref="order_items"
    )

    size = Column(
        String(5), 
        primary_key=True,
        nullable= False
    )

    qty = Column(Integer, default=1)

    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))