import datetime
import json
import random
import string
from datetime import timedelta

from faker import Faker
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker

from app.models.cart import cart_item_model, cart_model
from app.models.product import product_model
from app.models.user import user_model

engine = create_engine('mysql+mysqldb://root:test123!!!@127.0.0.1:3306/fastapi_ec_db')

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()


def get_user():
    user = session.query(user_model.User).filter(user_model.User.id == "b57d552082804a55823b0d49ec1e2082").first()
    return user


def create_cart():
    cart = cart_model.Cart(user_id="b57d552082804a55823b0d49ec1e2082")
    session.add(cart)
    session.commit()

def add_item_to_cart():
    cart = session.query(cart_model.Cart).filter(cart_model.Cart.user_id == "b57d552082804a55823b0d49ec1e2082").first()

    
   
    #已經存在，就+1
    #應該取cart_item的id才對
    #總共要給:user_id / cart_item.id / 從cart_item取product_id
    #先判斷是否存在於user.cart.cart_item??
    #還是直接判斷cart_item table是否有一個product_id和當前一樣的 ->不對，這樣其他購物車加同個產品不就gg = = 所以應該是同個pro_id+user_id的組合才對!!! 不對

    product_id = "3b4f0e2dd1384cb5be045d66c31ab08f"
    cart_id = "683be32449744bfc881219449ce38f05"

    cart_item = session.query(cart_item_model.CartItem).filter(cart_item_model.CartItem.product_id == product_id,cart_item_model.CartItem.cart_id == cart_id).first() 


    if cart_item:
        cart_item.quantity += 1
        
    else:
        
        #找產品
        product = session.query(product_model.Product).filter(product_model.Product.id == "3b4f0e2dd1384cb5be045d66c31ab08f").first()

        print(product.product_name,'這是product')

        #創建cart_item
        # item = cart_item_model.CartItem(quantity=2,product_id = product.id, cart_id = cart.id)
        item = cart_item_model.CartItem(quantity=2,product_id = product.id, cart_id = cart.id)
        session.add(item)


        print(item.cart_id,'這是item')
        
        #總之問題永遠就是: item找不到他關聯的cart
        #試過: 
        #1.item =xxxx之後session.add(item) -> 因為還沒被加入cart所以無法拿到cart id 
        #2.item=xxx之後 直接append到cart ，再session.add(cart) -> commit -> 不行，item還是沒法找到cart喔@
        cart.cart_items.append(item)
    session.commit()
    

def get_user_cart():
    user = get_user()
    # print(user.cart[0].cart_items[0].quantity,'這是user的cart數量')
    # print(user.cart,'這是user的cart')
    # for cart in user.cart:
    #     for item in cart.cart_items:
    #         print(cart.id,'cart id喔@')
    #         print(item.product.product_name,'名稱')

    # print(jsonable_encoder(user.cart.cart_items[0].product),'cart_items第一個')
    print(jsonable_encoder(user.cart.cart_items),'cart_items')

    # print(jsonable_encoder(user.cart),'cart')
    # print(jsonable_encoder(user),'第一個')


def remove_from_cart():
    product_id = "3b4f0e2dd1384cb5be045d66c31ab08f"
    cart_id = "683be32449744bfc881219449ce38f05"

    cart_item = session.query(cart_item_model.CartItem).filter(cart_item_model.CartItem.product_id == product_id,cart_item_model.CartItem.cart_id == cart_id).first()

    cart = session.query(cart_model.Cart).filter(cart_model.Cart.user_id == "b57d552082804a55823b0d49ec1e2082").first()

    # for item in cart.cart_items:
    #     print(item.product_id,'產品id')
    #     print(item.cart_id,'cart id')
    session.delete(cart_item)
    session.commit()

    
# add_item_to_cart()
#remove_from_cart()
get_user_cart()
