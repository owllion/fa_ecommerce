import uuid
from datetime import datetime

from sqlalchemy import (
    DECIMAL,
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    text,
)

from ...database.db import Base


class Coupon(Base):
    __tablename__ = 'coupon'

    id = Column(String(36), primary_key=True, index=True,default=str(uuid.uuid4()))

    user_id = Column(String(36), ForeignKey('user.id'), nullable=False)

    code = Column(String(255), nullable=False, index=True)

    description = Column(Text,default="")

    amount = Column(DECIMAL(10, 2), nullable=False)

    expiry_date = Column(TIMESTAMP, nullable=False)

    minimum_amount = Column(DECIMAL(10, 2), nullable=False)

    discount_type = Column(String(255), nullable=False)

    is_used = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))
   