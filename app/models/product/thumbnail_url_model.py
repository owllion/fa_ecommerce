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


class ThumbnailUrl(Base):
    __tablename__ = 'thumbnail_url'

    id = Column(String(36), primary_key=True, index=True,default=str(uuid.uuid4()))

    url = Column(String(350), nullable= False)

    product_id = Column(String(36), ForeignKey("product.id",ondelete="CASCADE"),nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))