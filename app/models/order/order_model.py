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


class OrderStatus(int,Enum):
    COMPLETED = 0
    CANCELED = 1
class PaymentStatus(int,Enum):
    PAID = 0

class Order(Base):
    __tablename__ = 'order'

    id = Column(String(36), primary_key=True, index=True,default=str(uuid.uuid4()))

    order_status = Column(Integer, default=OrderStatus.COMPLETED) 

    # order_id = Column(String(10), unique=True, nullable=False)

    owner = relationship("User", back_populates="orders")

    owner_id = Column(Integer, ForeignKey('user.id',ondelete="CASCADE"),nullable=False)

    order_items = relationship("OrderItem", back_populates="parent_order",cascade="all, delete",passive_deletes=True)


    delivery_address = Column(String(200), nullable=False)

    discount = Column(Float, default=0)
    
    discount_code = Column(String(10), default="")

    total = Column(Float, nullable=False)

    discount_total = Column(Float, default=0)

    shipping = Column(Float, nullable=False)

    receiver_name = Column(String(50), nullable=False)

    payment_method = Column(String(20), default="credit_card")

    payment_status = Column(Integer, default=PaymentStatus.PAID) 

    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

