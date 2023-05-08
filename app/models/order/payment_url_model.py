import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import relationship

from ...database.db import Base
from ...utils.common.generate_id import gen_id


class PaymentUrl(Base):
    __tablename__ = "payment_url"

    order_id = Column(
        String(80), ForeignKey("order.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )

    url = Column(String(300))  # 可以是null/字串/沒有預設/不是pk

    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
