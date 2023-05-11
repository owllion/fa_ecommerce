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


class OrderStatus(int, Enum):
    COMPLETED = 0
    CANCELED = 1


class PaymentStatus(int, Enum):
    PENDING_PAYMENT = 0
    PAID = 1


class PaymentMethods(str, Enum):
    credit_card = "credit_card"
    line_pay = "line_pay"


class Order(Base):
    __tablename__ = "order"

    id = Column(String(80), primary_key=True, index=True, default=gen_id)

    order_status = Column(Integer, default=OrderStatus.COMPLETED.value, nullable=False)

    # order_id = Column(String(10), unique=True, nullable=False)

    owner = relationship("User", back_populates="orders")

    owner_id = Column(String(80), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    order_items = relationship(
        "OrderItem", back_populates="parent_order", cascade="all, delete", passive_deletes=True
    )

    delivery_address = Column(String(200), nullable=False)

    discount = Column(Float, default=0)

    discount_code = Column(String(10), default="")

    total = Column(Float, nullable=False)

    discount_total = Column(Float, default=0)

    shipping = Column(Float, nullable=False)

    receiver_name = Column(String(50), nullable=False)

    payment_method = Column(String(20), default=PaymentMethods.credit_card.value, nullable=False)

    payment_status = Column(Integer, default=PaymentStatus.PENDING_PAYMENT.value, nullable=False)

    payment_url = relationship(
        "PaymentUrl",
        backref="related_order",
        cascade="all, delete",
        passive_deletes=True,
        uselist=False,
    )  # backref/back_poopulat皆可 後面兩個選項是當這個order被刪除後 對應的payment_url也會被刪除
    # uselist=False 表示這是1對1，這個值不會是list，而是會是一個dict

    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    def copy(self):
        print("呼叫copy")
        new = Order()
        new.delivery_address = self.delivery_address
        new.discount = self.discount
        new.discount_code = self.discount_code
        new.order_status = self.order_status
        new.owner_id = self.owner_id

        for item in self.order_items:
            new.order_items.append(item.copy())
        return new

    def clone(self):
        d = dict(self.__dict__)
        d.pop("id")  # get rid of id
        d.pop("_sa_instance_state")  # get rid of SQLAlchemy special attr
        copy = self.__class__(**d)
        for item in self.order_items:
            copy.order_items.append(item.copy())

        return copy
