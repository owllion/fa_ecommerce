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

from ...database.db import Base


class Like(Base):
    __tablename__ = "like"

    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)

    product_id = Column(Integer, ForeignKey('products.id',ondelete="CASCADE"), primary_key=True)

    user = relationship('User', back_populates='like_items')
    
    product = relationship('Product', backref='likes')

    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))