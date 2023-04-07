import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship

from ..database.db import Base


class Product(Base):
    __tablename__ = 'product'

    id = Column(String(36), primary_key=True, index=True,default=str(uuid.uuid4()))

    # product_id = Column(String, nullable=False, unique=True, index=True)
    product_name = Column(String(50), nullable=False)

    thumbnail = Column(String(100), nullable=False)

    price = Column(Float, nullable=False)

    brand = Column(String, nullable=False)

    category = Column(String, nullable=False)
    size = Column(String, default="F")
    color = Column(String, default="")
    description = Column(String, default="")
    stock = Column(Integer, nullable=False)
    availability = Column(Boolean, nullable=False)
    sales = Column(Integer, nullable=False)
    qty = Column(Integer)
    is_checked = Column(Boolean, default=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    
    image_list = Column(String, nullable=False)
    thumbnail_list = Column(String, nullable=False)

    reviews = relationship("Review", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.product_name}')>"
