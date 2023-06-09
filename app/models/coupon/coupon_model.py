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
from ...utils.common.generate_id import gen_id


class Coupon(Base):
    __tablename__ = "coupon"

    id = Column(String(80), primary_key=True, index=True, default=gen_id)

    code = Column(String(255), nullable=False, index=True)

    related_user_coupons = relationship(
        "UserCoupon",
        back_populates="coupon",
        cascade="all, delete",
        passive_deletes=True,
    )

    description = Column(Text, default="")

    amount = Column(DECIMAL(10, 2), nullable=False)

    expiry_date = Column(TIMESTAMP, nullable=False)

    minimum_amount = Column(DECIMAL(10, 2), nullable=False)

    discount_type = Column(String(255), nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
