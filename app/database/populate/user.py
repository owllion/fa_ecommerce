import datetime
import json
import random
import string
from datetime import timedelta

from decouple import config
from faker import Faker
from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker

from app.models.user import user_model

engine = create_engine('mysql+mysqldb://root:test123!!!@127.0.0.1:3306/fastapi_ec_db')

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

def generate_code(length=10):
    return ''.join(random.choices(string.digits, k=length))

for _ in range(300):
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone = generate_code()
    password = fake.password()
    upload_avatar = fake.image_url()
    default_avatar = config('DEFAULT_AVATAR_URL')
    verified = random.choice([True, False])

    user = user_model.User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        password=password,
        upload_avatar=upload_avatar,
        default_avatar=default_avatar,
        verified=verified
    )
    session.add(user)

session.commit()