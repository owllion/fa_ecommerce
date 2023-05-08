import uuid
from datetime import datetime
from enum import Enum

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
from ...schemas.user_schema import LoginTypeValue
from ...utils.common import generate_id


class LoginType(Base):
    __tablename__ = "login_type"

    id = Column(String(80), primary_key=True, index=True, default=generate_id.gen_id)

    value = Column(String(20), default=LoginTypeValue.EMAIL)

    related_login_type = relationship(
        "UserLoginType", back_populates="type", cascade="all, delete", passive_deletes=True
    )

    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
