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
from ...utils.common.generate_id import gen_id


class Cart(Base):
    __tablename__ = "cart"

    id = Column(String(80), primary_key=True, index=True, default=gen_id)

    user_id = Column(String(80), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    relate_user = relationship("User", back_populates="cart")

    cart_items = relationship(
        "CartItem", back_populates="parent_cart", cascade="all, delete", passive_deletes=True
    )

    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
