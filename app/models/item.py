from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Text
from sqlalchemy.orm import relationship
import uuid

from ..database.db import Base


class Item(Base):
    __tablename__ = "item"

    id = Column(String(36), primary_key=True, index=True,default=str(uuid.uuid4()))
    title = Column(String(60), index=True)
    description = Column(Text(), index=True)
    owner_id = Column(String(36), ForeignKey("user.id"))

    owner = relationship("User", back_populates="items")

