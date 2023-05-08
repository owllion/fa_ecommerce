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


class Size(Base):
    __tablename__ = "size"

    id = Column(String(80), primary_key=True, index=True, default=gen_id)

    value = Column(String(5), nullable=False)

    related_product_item = relationship(
        "ProductItem", back_populates="size", cascade="all, delete", passive_deletes=True
    )

    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
