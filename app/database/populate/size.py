
import random
import string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.product import size_model

engine = create_engine('mysql+mysqldb://root:test123!!!@127.0.0.1:3306/fastapi_ec_db')

Session = sessionmaker(bind=engine)
session = Session()

def generate_code(length=10):
    return ''.join(random.choices(string.digits, k=length))

sizes = ['XS','S','M','L','XL']

for s in sizes:
    size = size_model.Size(
        size=s 
    )
    session.add(size)

session.commit()