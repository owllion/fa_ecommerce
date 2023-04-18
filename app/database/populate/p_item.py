import random

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.product import product_item_model, product_model, size_model

engine = create_engine('mysql+mysqldb://root:test123!!!@127.0.0.1:3306/fastapi_ec_db')

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

#1. 找到所有products -> 拿到每個產品id -> 存起來
#2. 找到所有sizes -> 跑回圈把所有id存在list裡
#3. products跑回圈 p_id(外層products)/s_id(內層)/stock/sales

pIds = []
sIds = []
products = session.query(product_model.Product).all()
sizes = session.query(size_model.Size).all()

for p in products:
    pIds.append(p.id)
for s in sizes:
    sIds.append(s.id)


for pid in pIds:
    for sid in sIds:
        p_item = product_item_model.ProductItem(
            product_id = pid,
            size_id = sid,
            stock = random.randint(1, 1000),
            sales = random.randint(1, 1000)
        )
        session.add(p_item)

session.commit()

