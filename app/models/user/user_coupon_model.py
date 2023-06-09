import uuid
from datetime import datetime

from sqlalchemy import (
    DECIMAL,
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

from ...database.db import Base


class UserCoupon(Base):
    __tablename__ = "user_coupon"

    user_id = Column(String(80), ForeignKey("user.id"), primary_key=True, nullable=False)

    coupon_id = Column(String(80), ForeignKey("coupon.id"), primary_key=True, nullable=False)

    coupon = relationship("Coupon", back_populates="related_user_coupons")

    is_used = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
