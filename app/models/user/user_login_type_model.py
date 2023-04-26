import uuid
from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import relationship

from ...database.db import Base


class UserLoginType(Base):
    __tablename__ = "user_login_type"

    user_id = Column(
        String(80), 
        ForeignKey(
            'user.id', 
            ondelete="CASCADE"
        ), 
        primary_key=True
    )

    login_type_id = Column(
        String(80), 
        ForeignKey(
            "login_type.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    type = relationship("LoginType",back_populates="related_login_type", uselist=False)
   

    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))