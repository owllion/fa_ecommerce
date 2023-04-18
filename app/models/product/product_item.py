import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import relationship

from ...database.db import Base
from ...utils.generate_id import gen_id


#每個product的5個size的資料
class ProductItem(Base):
    __tablename__ = 'ProductItem'

    size_id = Column(String(80), ForeignKey("size.id",ondelete="CASCADE"),nullable=False)
    
    size = relationship("Size",backref="related_product_item")

    stock = Column(Integer, nullable=False)

    sales = Column(Integer, nullable=False)

    product_id = Column(String(80), ForeignKey("product.id",ondelete="CASCADE"),nullable=False)


    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))