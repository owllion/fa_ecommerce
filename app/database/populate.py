import json
import random

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.product import (
    product_image_url_model,
    product_model,
    thumbnail_url_model,
)

# from ..models.product import product_model

# from app.models.review import review_model
# from app.models.user import user_model

engine = create_engine('mysql+mysqldb://root:test123!!!@127.0.0.1:3306/fastapi_ec_db')

Session = sessionmaker(bind=engine)
session = Session()

# review = review_model.Review(user_id="b57d552082804a55823b0d49ec1e2082",product_id="00f1f8cd3b3e4bf6a6ff3db0d20141e7", rating=4.0, comment='Good product')
# session.add(review)
# session.commit()
# review = session.query(review_model.Review).get("cf7a911983444389bdf5d49cf80feb23")
# user = session.query(user_model.User).filter(user_model.User.id == "b57d552082804a55823b0d49ec1e2082").first()



# with open('products.json', 'r',encoding='utf-8') as file:
#     products = json.load(file)
#     for product in products:
#         new_product = product_model.Product(
#             product_name=product['productName'],
#             price=product['price'],
#             brand=product['brand'],
#             category=product['category'],
#             description=product['description'],
#             stock=product['stock'],
#             availability=product['availability'],
#             sales=product['sales'],
#             is_checked=product['isChecked'],
#             color=product['color'],
#             thumbnail=product['thumbnail'],
#         )
#         session.add(new_product)
#         session.commit()

fake = Faker()
# category = ["blazer","shirt","knitwear","tshirt","coat","hat","trouser"]
# brand = ["Givenchy","Gucci","Lenon","Lululemon","Dior","Cartier"]
# for _ in range(81):
#     new_product = product_model.Product(
#         product_name=fake.word() + ' ' + fake.word() + ' ' + fake.word(),
#         price=random.randint(100, 1000),
#         brand=random.choice(brand),
#         category=random.choice(category),
#         description=fake.paragraph(nb_sentences=3),
#         stock=random.randint(100, 1000),
#         availability=random.choice([True, False]),
#         sales= random.randint(0, 1000),
#         is_checked=random.choice([True, False]),
#         color=fake.color_name(),
#         thumbnail=fake.image_url(width=320, height=400)
#     )
#     session.add(new_product)
#     session.commit()


db_products = session.query(product_model.Product).all()
def get_id_from(name: str):
    for p in db_products:
        if p.product_name == name: return p.id

for _ in range(80):
    # fake.image_url(width=320, height=400)

    # imageurl = thumbnail_url_model.ThumbnailUrl(
    #     url =fake.image_url(width=720, height=900),product_id =get_id_from(product['productName']) 
    # )
    
    imageurl = thumbnail_url_model.ThumbnailUrl(
        url =fake.image_url(width=320, height=400),product_id =get_id_from(product['productName']) 
    )

    session.add(imageurl)
    session.commit()

   
    







# with open('products.json', 'r',encoding='utf-8') as file:
#     products = json.load(file)

#     for product in products:
#         for url in product['thumbnailList']:
#             imageurl = thumbnail_url_model.ThumbnailUrl(url = url,product_id =get_id_from(product['productName']) )

#             session.add(imageurl)
#             session.commit()






