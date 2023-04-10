import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from ...database.db import Base
from ...utils.generate_id import gen_id


class Review(Base):
    __tablename__ = 'review'

    id = Column(String(80), primary_key=True, index=True,default=gen_id)

    user_id = Column(String(80), ForeignKey('user.id',ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="reviews")

    product_id = Column(String(80), ForeignKey('product.id',ondelete="CASCADE"), nullable=False)

    product = relationship("Product", back_populates="reviews")

    # review_id = Column(String(), nullable=False)
    
    rating = Column(Float, nullable=False)
    
    comment = Column(String(300), nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))