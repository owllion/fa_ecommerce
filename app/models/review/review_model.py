import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database.db import Base


class Review(Base):
    __tablename__ = 'review'

    id = Column(String(36), primary_key=True, index=True,default=str(uuid.uuid4()))

    user_id = Column(Integer, ForeignKey('user.id'), ondelete="CASCADE",nullable=False)

    user = relationship("User", back_populates="reviews")

    product_id = Column(Integer, ForeignKey('product.id'), ondelete="CASCADE" ,nullable=False)

    product = relationship("Product", back_populates="reviews")

    # review_id = Column(String(), nullable=False)
    
    rating = Column(Float, nullable=False)
    
    comment = Column(String(300), nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now)
    
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)