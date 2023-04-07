import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database.db import Base


class Cart(Base):
    __tablename__ = "cart"

    id = Column(String(36), primary_key=True, index=True,default=str(uuid.uuid4()))

    user_id = Column(Integer, ForeignKey("user.id"),ondelete="CASCADE",nullable=False)

    