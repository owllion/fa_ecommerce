from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import uuid
from ..database.db import Base,engine


class User(Base):
    __tablename__ = "user"

    id = Column(String(36), primary_key=True, index=True,default=str(uuid.uuid4()))
    email = Column(String(80), unique=True,index=True)
    hashed_password = Column(String(80))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

