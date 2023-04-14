import datetime
import json
import random
import string
from datetime import timedelta

from faker import Faker
from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker

from app.models.coupon import coupon_model

engine = create_engine('mysql+mysqldb://root:test123!!!@127.0.0.1:3306/fastapi_ec_db')

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

"""
pydecimal:
    left_digits:整數位的位數
    right_digits:小數位的位數(0->沒有小數點)
    positive:生成的數字是否為正數
"""

def generate_code(length=6):
    letters_digits = string.ascii_letters + string.digits
    #0123456798 + a-z
 
    return ''.join(random.choices(letters_digits, k=length))
    #random returns [choices*k], so use join

for _ in range(200):
    coupon = coupon_model.Coupon(
        code=generate_code(),
        description=fake.sentence(),
        amount=fake.pydecimal(left_digits=2, right_digits=0, positive=True),
        expiry_date=datetime.datetime.now() + timedelta(weeks=fake.random_int(min=1, max=50)),
        minimum_amount=fake.pydecimal(left_digits=2, right_digits=0, positive=True),
        discount_type=fake.random_element(elements=("fixed_amount", "percentage")),
        is_used=False,
    )
    session.add(coupon)

session.commit()








