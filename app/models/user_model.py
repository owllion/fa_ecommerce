from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,TIMESTAMP,text,event
from sqlalchemy.orm import relationship
import uuid
from decouple import config

from ..database.db import Base
from ..utils import security

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

@event.listens_for(User, 'before_insert')
@event.listens_for(User, 'before_update')
def hash_password(mapper, connection, target):
    """
    Hash the password before saving it to the database.
    """
    if target.password and not security.is_hashed_password(target.password):
        security.hash_password(target.password)

        