import random

from faker import Faker

fake = Faker()

# 產生隨機商品資料
product_name = fake.word() + ' ' + fake.word() + ' ' + fake.word()
price = random.randint(100, 1000)
sale_price = int(price * random.uniform(0.2, 0.8))
brand = fake.company()
category = fake.word()
description = fake.paragraph(nb_sentences=3)
stock = random.randint(100, 1000)
availability = random.choice([True, False])
sales = random.randint(0, 1000)
is_checked = random.choice([True, False])
product_id = fake.uuid4()
color = fake.color_name()
thumbnail = fake.image_url(width=320, height=400)
image_list = [
    fake.image_url(width=720, height=900),
    fake.image_url(width=720, height=900),
    fake.image_url(width=720, height=900)
]
thumbnail_list = [
    fake.image_url(width=320, height=400),
    fake.image_url(width=320, height=400),
    fake.image_url(width=320, height=400)
]

# 產生 MySQL 的 INSERT 語句
query = f"INSERT INTO products (productName, price, salePrice, brand, category, description, stock, availability, sales, isChecked, productId, color, thumbnail, imageList, thumbnailList) VALUES ('{product_name}', {price}, {sale_price}, '{brand}', '{category}', '{description}', {stock}, {availability}, {sales}, {is_checked}, '{product_id}', '{color}', '{thumbnail}', '{str(image_list)}', '{str(thumbnail_list)}');"
print(query)
