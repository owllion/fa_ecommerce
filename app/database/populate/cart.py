import datetime
import json
import random
import string
from datetime import timedelta

from faker import Faker
from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker

from app.models.cart import cart_item_model, cart_model
from app.models.user import user_model

engine = create_engine('mysql+mysqldb://root:test123!!!@127.0.0.1:3306/fastapi_ec_db')

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()


def get_users():
    return session.query(user_model.User).all()
# def get_coupons():
#     return session.query(coupon_model.Coupon).all()

def add_item_to_cart():

    users = get_users()
    coupons = get_coupons()
    
    random_10_coupons = random.choices(coupons,k=10)

    for user in users:
        user.coupons.extend(random_10_coupons)

    session.commit()

def add_one_coupon_to_user():
    user = session.query(user_model.User).filter(user_model.User.id == "b57d552082804a55823b0d49ec1e2082").first()

    coupon = session.query(coupon_model.Coupon).filter(coupon_model.Coupon.code=="PyGloL").first()
    user.coupons.append(coupon)
    session.commit()
    

