from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,TIMESTAMP,text,Text
from sqlalchemy.orm import relationship
import uuid
from ..database.db import Base

class Item(Base):
    __tablename__ = "item"

    id = Column(String(36), primary_key=True, index=True,default=str(uuid.uuid4()))
    title = Column(String(60), index=True)
    description = Column(String(600), index=True)
    owner_id = Column(String(36), ForeignKey("user.id"))
    created_at = Column(
        TIMESTAMP(timezone=True),nullable=False, 
        server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False, 
        server_default=text("now()")
    )

    owner = relationship("User", back_populates="items")

