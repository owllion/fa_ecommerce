from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,TIMESTAMP,text
from sqlalchemy.orm import relationship
import uuid
from ..database.db import Base,engine
from decouple import config

class User(Base):
    __tablename__ = "user"

    id = Column(String(36), primary_key=True, index=True,default=str(uuid.uuid4()))
    email = Column(String(80), unique=True,index=True)
    username = Column(String(30), index=True)
    password = Column(String(80))

    upload_avatar = Column(String(100), nullable=True,default='')

    default_avatar = Column(String(100), default= config('DEFAULT_AVATAR_URL'))

    verified = Column(Boolean, nullable=False,default=False)

    created_at = Column(
        TIMESTAMP(timezone=True),nullable=False, 
        server_default=text("now()")
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False, 
        server_default=text("now()")
    )

    items = relationship("Item", back_populates="owner")

