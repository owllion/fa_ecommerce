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


class Cart(Base):
    __tablename__ = "cart"

    id = Column(String(36), primary_key=True, index=True,default=str(uuid.uuid4()))

    user_id = Column(Integer, ForeignKey("user.id",ondelete="CASCADE"),nullable=False)

    relate_user = relationship("User",back_populates="cart")

    cart_items = relationship("CartItem", back_populates="parent_cart",cascade="all, delete",passive_deletes=True)

    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

    