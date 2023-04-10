import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.product import product_model

# 建立資料庫引擎
engine = create_engine('mysql+mysqldb://root:test123!!!@127.0.0.1:3306/fastapi_ec_db')

# 建立 Session 類別實例
Session = sessionmaker(bind=engine)
session = Session()

# 開啟 JSON 文件，讀取內容並加入 MySQL 資料庫
with open('products.json', 'r',encoding='utf-8') as file:
    products = json.load(file)
    for product in products:
        new_product = product_model.Product(
            product_name=product['productName'],
            price=product['price'],
            brand=product['brand'],
            category=product['category'],
            description=product['description'],
            stock=product['stock'],
            availability=product['availability'],
            sales=product['sales'],
            is_checked=product['isChecked'],
            color=product['color'],
            thumbnail=product['thumbnail'],
        )
        session.add(new_product)
        session.commit()
