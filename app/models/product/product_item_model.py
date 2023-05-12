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
from ...utils.common.generate_id import gen_id


class ProductItem(Base):
    __tablename__ = "product_item"

    product_id = Column(
        String(80), ForeignKey("product.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )

    parent_product = relationship("Product", back_populates="product_items")

    size_id = Column(
        String(80), ForeignKey("size.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )

    size = relationship("Size", back_populates="related_product_item", uselist=False)
    # 這邊用bp是因為 1.需要size值 2.size model也必須得寫一個欄位，因為要設定cascade之類的 -> 兩邊都各自需要寫個關聯欄位

    stock = Column(Integer, nullable=False)

    sales = Column(Integer, nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
