from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from uuid import UUID

from ..database.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True,index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
