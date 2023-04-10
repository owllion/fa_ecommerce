import uuid

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.orm import relationship

from ..database.db import Base


class Item(Base):
    __tablename__ = "item"

    id = Column(String(80), primary_key=True, index=True,default=str(uuid.uuid4))
    title = Column(String(60), index=True)
    description = Column(String(600), index=True)
    owner_id = Column(String(80), ForeignKey("user.id"))
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

