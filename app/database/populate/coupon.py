import datetime
import json
import random
import string
from datetime import timedelta

from faker import Faker
from sqlalchemy import and_, create_engine, func
from sqlalchemy.orm import sessionmaker

from app.models.coupon import coupon_model
from app.models.user import user_coupon_model, user_model

engine = create_engine("mysql+mysqldb://root:test123!!!@127.0.0.1:3306/fastapi_ec_db")

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()


def generate_code(length=6):
    letters_digits = string.ascii_letters + string.digits
    # 0123456798 + a-z

    return "".join(random.choices(letters_digits, k=length))
    # random returns [choices*k], so use join


def add_coupon():
    """
    pydecimal:
        left_digits:整數位的位數
        right_digits:小數位的位數(0->沒有小數點)
        positive:生成的數字是否為正數
    """
    for _ in range(1):
        coupon = coupon_model.Coupon(
            code=generate_code(),
            description=fake.sentence(),
            amount=fake.pydecimal(left_digits=2, right_digits=0, positive=True),
            expiry_date=datetime.datetime.now()
            + timedelta(milliseconds=fake.random_int(min=1, max=50)),
            minimum_amount=fake.pydecimal(left_digits=2, right_digits=0, positive=True),
            discount_type=fake.random_element(elements=("fixed_amount", "percentage")),
            is_used=False,
        )
        session.add(coupon)

    session.commit()


def get_users():
    return session.query(user_model.User).all()


def get_coupons():
    return session.query(coupon_model.Coupon).all()


def add_coupon_to_user():
    users = get_users()
    # coupons = get_coupons()
    user = session.query(user_model.User).filter_by(id="b57d552082804a55823b0d49ec1e2082").all()

    random_ten = session.query(coupon_model.Coupon.id).order_by(func.random()).limit(10).all()

    ten_ids = [id for id, in random_ten]
    print(ten_ids[0], "這是ten_ids")
    for u in user:
        # 美人產生10筆
        for id in ten_ids:
            res = user_coupon_model.UserCoupon(user_id=u.id, coupon_id=id)
            session.add(res)
    session.commit()


def add_one_coupon_to_user():
    user = (
        session.query(user_model.User)
        .filter(user_model.User.id == "b57d552082804a55823b0d49ec1e2082")
        .first()
    )

    coupon = (
        session.query(coupon_model.Coupon).filter(coupon_model.Coupon.code == "PyGloL").first()
    )
    user.coupons.append(coupon)
    session.commit()


# add_coupon()
# add_one_coupon_to_user()
add_coupon_to_user()
