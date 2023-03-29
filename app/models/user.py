from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database.db import Base,engine


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(80), unique=True,index=True)
    hashed_password = Column(String(80))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

Base.metadata.create_all(engine)