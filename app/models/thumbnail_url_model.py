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

from ..database.db import Base


class ThumbnailUrl(Base):
    __tablename__ = 'thumbnail_url'

    url = Column(String(350), nullable= False)

    product_id = Column(Integer, ForeignKey("product.id"),ondelete="CASCADE",nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),nullable=False, 
        server_default=text("now()")
    )

    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()"))