import uuid
from enum import Enum
from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database.db import Base


class OrderStatus(int,Enum):
    COMPLETED = 0
    CANCELED = 1
class PaymentStatus(int,Enum)

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    order_status = Column(Integer, default=OrderStatus.COMPLETED) 

    order_id = Column(String(10), unique=True, nullable=False)

    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    delivery_address = Column(String(100), nullable=False)

    discount = Column(Float, default=0)
    
    discount_code = Column(String(10), default="")

    total = Column(Float, nullable=False)

    discount_total = Column(Float, default=0)

    shipping = Column(Float, nullable=False)

    receiver_name = Column(String(50), nullable=False)

    payment_method = Column(String(20), default="credit_card")

    payment_status = Column(Integer, default=0) # 0 -> paid

    payment_date = Column(DateTime, default=datetime.now())


    created_at = Column(
        TIMESTAMP(timezone=True),nullable=False, 
        server_default=text("now()")
    )

    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()"))

    owner = relationship("User", back_populates="orders")