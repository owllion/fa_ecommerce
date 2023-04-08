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


class Cart(Base):
    __tablename__ = "like"
    
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)

    user = relationship('User', back_populates='like_items')
    
    product = relationship('Product', backref='likes')

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)