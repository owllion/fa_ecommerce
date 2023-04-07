import uuid

from decouple import config
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, event, text
from sqlalchemy.orm import relationship

from ..database.db import Base
from ..utils import security


class User(Base):
    __tablename__ = "user"

    id = Column(String(36), primary_key=True, index=True,default=str(uuid.uuid4()))
    email = Column(String(80), unique=True,index=True)
    first_name = Column(String(30), index=True)
    last_name = Column(String(30), index=True)
    phone = Column(String(15), nullable=True,default='')
    password = Column(String(80))
    upload_avatar = Column(String(350), nullable=True,default='')
    default_avatar = Column(String(350), default= config('DEFAULT_AVATAR_URL'))

    verified = Column(Boolean, nullable=False,default=False)



    created_at = Column(
        TIMESTAMP(timezone=True),nullable=False, 
        server_default=text("now()")
    )

    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()"))

    items = relationship("Item", back_populates="owner")

    #cartList
    cart_items = relationship("Cart", back_populates="user")

    like_items = relationship("Like", back_populates="user")
    orders = relationship("Order", back_populates="owner")
    reviews = relationship("Review", back_populates="user")

@event.listens_for(User, 'before_insert')
@event.listens_for(User, 'before_update')
def hash_password(mapper, connection, target):
    """
    Hash the password before saving it to the database.
    """
    if target.password and not security.is_hashed_password(target.password):
        target.password = security.hash_password(target.password)
