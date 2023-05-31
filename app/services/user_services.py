from decouple import config
from fastapi import Depends, HTTPException, Request, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from ..constants import api_msgs, constants
from ..database import db
from ..exceptions.main import raise_http_exception
from ..models.cart import cart_item_model, cart_model
from ..models.user import user_model
from ..schemas import email_schema, user_schema
from ..schemas.cart_schema import OperationType
from ..utils.email import email
from ..utils.security import security
from . import coupon_services


def find_user_with_email(email: str, db: Session = Depends(db.get_db)):
    user = (
        db.query(user_model.User).filter(user_model.User.email == EmailStr(email.lower())).first()
    )

    return user


def find_user_with_id(id: str, db: Session = Depends(db.get_db)):
    user = db.query(user_model.User).filter(user_model.User.id == id).first()

    return user


def svc_create_user(payload: user_schema.UserCreateSchema, db: Session):
    # payload from github login is already a dictionary,no need to use .dict() to convert it again.
    if type(payload) is dict:
        new_user = user_model.User(**payload)
    else:
        new_user = user_model.User(**payload.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_updated_payload_data(payload: user_schema.UserCreateSchema):
    payload.password = security.hash_password(payload.password)
    payload.email = EmailStr(payload.email.lower())

    return payload


def user_is_verified(verified: bool):
    if not verified:
        raise_http_exception(api_msgs.EMAIL_NOT_VERIFIED, status.HTTP_401_UNAUTHORIZED)
    return True


def password_is_matched(payload_pwd: str, user_pwd: str):
    if not security.verify_password(payload_pwd, user_pwd):
        raise_http_exception(api_msgs.INCORRECT_LOGIN_INPUT)
    return True


async def send_link(payload: email_schema.SendLinkSchema):
    token = security.create_token(
        payload.user_id,
        payload.token_type,
    )

    target_link = f'{config("FRONTEND_DEPLOY_URL")}/auth/{payload.url_params}/{token}'

    await email.send_link(
        {"type": payload.link_type, "link": target_link, "email": payload.user_email}
    )


def get_item_from_user_cart(req: Request, product_id: str, size: str):
    def find_item(item: cart_item_model.CartItem, id: str, size: str):
        print(item.product_id, "這是item.pr_id")
        print(id, "收到的product_id")
        print(item.size, "this is item.size")
        print(size, "收到的size")
        if item.product_id == id and item.size == size:
            return True
        return False

    cart_item = list(
        filter(lambda x: find_item(x, product_id, size), req.state.mydata.cart.cart_items)
    )

    return cart_item[0] if cart_item else None


def get_user_cart_id(req: Request):
    return req.state.mydata.cart.id


def get_item_from_cart_item_table(req: Request, product_id: str, db: Session):
    user_cart_id = get_user_cart_id(req)

    cart_item = (
        db.query(cart_item_model.CartItem)
        .filter(
            cart_item_model.CartItem.product_id == product_id,
            cart_item_model.CartItem.cart_id == user_cart_id,
        )
        .first()
    )

    if not cart_item:
        raise_http_exception(api_msgs.CART_ITEM_NOT_FOUND)
    return cart_item


def delete_item(db: Session, cart_item: cart_item_model.CartItem):
    db.delete(cart_item)
    db.commit()


def update_qty(cart_item: cart_item_model.CartItem, stock: int, operation_type: str, db: Session):
    # 確認完當前購物車內數量是正常的之後(超過就會error)
    # 是按下+ -> 判斷加上去是否會>stock，會就error
    # 按下 - -> 判斷減去是否會<1(前端確認即可，但後端為了保險還是要確認)
    if cart_item.quantity > 1 and cart_item.quantity < stock:
        cart_item.quantity += 1 if operation_type == OperationType.INC else -1
        db.commit()
        # 在購物車裡面做更新，qty只會是+1(因為不給手動輸入)
    else:
        raise_http_exception(api_msgs.CART_ITEM_QUANTITY_LIMITS_ERROR)


def find_user_with_github_username(name: str, db: Session):
    user = db.query(user_model.User).filter_by(github_username=name).first()

    return user


def gen_user_info_and_tokens(user: user_model.User, cart_length: int):
    return {
        "token": security.create_token(user.id, constants.TokenType.ACCESS),
        "refresh_token": security.create_token(user.id, constants.TokenType.REFRESH),
        "user": user,
        "cart_length": cart_length,
    }


def create_cart(user_id: str, db: Session):
    cart = cart_model.Cart(user_id=user_id)

    db.add(cart)
    db.commit()
    db.refresh(cart)


# when registering for the first time
def issue_coupons(user: user_model.User, db: Session):
    user.coupons.extend(coupon_services.get_first_ten_coupons(db))
    db.commit()
