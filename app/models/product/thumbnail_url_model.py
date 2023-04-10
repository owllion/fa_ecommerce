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


class ThumbnailUrl(Base):
    __tablename__ = 'thumbnail_url'

    id = Column(String(80), primary_key=True, index=True,default=gen_id)

    url = Column(String(350), nullable= False)

    product_id = Column(String(80), ForeignKey("product.id",ondelete="CASCADE"),nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))