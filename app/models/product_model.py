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

    brand = Column(String(30), nullable=False)

    category = Column(String, nullable=False)
    size = Column(String(10), default="F")
    color = Column(String(20),nullable=False)
    description = Column(String(800), default="")

    stock = Column(Integer, nullable=False)

    availability = Column(Boolean, nullable=False)

    sales = Column(Integer, nullable=False)

    qty = Column(Integer, default=1)

    is_checked = Column(Boolean, default=False)

    image_list = relationship("ProductImageUrl", backref="parent_product")

    thumbnail_list = relationship("ThumbnailUrl", backref="parent_product")

    reviews = relationship("Review", back_populates="product")

    

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.product_name}')>"
