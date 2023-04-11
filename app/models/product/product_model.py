import uuid
from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import relationship

from ...database.db import Base
from ...utils.generate_id import gen_id


class Product(Base):
    __tablename__ = 'product'

    id = Column(String(80), primary_key=True, index=True,default=gen_id)

    # product_id = Column(String, nullable=False, unique=True, index=True)
    product_name = Column(String(50), nullable=False)

    thumbnail = Column(String(100), nullable=False)

    price = Column(Float, nullable=False)

    brand = Column(String(30), nullable=False)

    category = Column(String(30), nullable=False)
    size = Column(String(10), default="F")
    color = Column(String(20),nullable=False)
    description = Column(String(800), default="")

    stock = Column(Integer, nullable=False)

    availability = Column(Boolean, nullable=False)

    sales = Column(Integer, nullable=False)

    qty = Column(Integer, default=1)

    is_checked = Column(Boolean, default=False)

    images = relationship("ProductImageUrl", backref="parent_product", cascade="all, delete",passive_deletes=True)

    thumbnails = relationship("ThumbnailUrl", backref="parent_product",cascade="all, delete",passive_deletes=True)

    reviews = relationship("Review", back_populates="product",cascade="all, delete",passive_deletes=True)


    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))


    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.product_name}')>"
