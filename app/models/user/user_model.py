import uuid

from decouple import config
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, event, text
from sqlalchemy.orm import relationship

from ...database.db import Base
from ...utils import generate_id, security


class User(Base):
    __tablename__ = "user"

    id = Column(String(80), primary_key=True, index=True,default=generate_id.gen_id)

    email = Column(String(80), unique=True,index=True)

    first_name = Column(String(30), index=True)

    last_name = Column(String(30), index=True)

    phone = Column(String(50), nullable=True,default='')

    password = Column(String(80))
    upload_avatar = Column(String(350), nullable=True,default='')

    default_avatar = Column(String(350), default= config('DEFAULT_AVATAR_URL'))

    verified = Column(Boolean, nullable=False,default=False)

    cart = relationship(
        "Cart", 
        back_populates="relate_user",cascade="all, delete",passive_deletes=True
    )

    favorites = relationship(
        "Product", 
        backref="users", secondary="user_favorite",cascade="all, delete",passive_deletes=True
    )

    coupons = relationship(
        "Coupon", 
        backref="users",
        secondary="user_coupon",
        cascade="all, delete",passive_deletes=True
    )

    orders = relationship(
        "Order", 
        back_populates="owner",
        cascade="all, delete",passive_deletes=True
    )

    reviews = relationship(
        "Review", 
        back_populates="user",
        cascade="all, delete",passive_deletes=True
    )

    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))


@event.listens_for(User, 'before_insert')
@event.listens_for(User, 'before_update')
def hash_password(mapper, connection, target):
    """
    Hash the password before saving it to the database.
    """
    if target.password and not security.is_hashed_password(target.password):
        target.password = security.hash_password(target.password)
