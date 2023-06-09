from functools import reduce

from decouple import config
from fastapi import Depends, Request, status
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..constants import api_msgs, constants
from ..database import db
from ..exceptions.main import raise_http_exception
from ..models.cart import cart_item_model, cart_model
from ..models.product import product_model
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
    # here payload's type is just a 'type', this is not an endpoint, so pydantic will not convert this 'payload' to paydantic obj, the payload you pass will remain what it is.
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
        payload["user_id"],
        payload["token_type"],
    )

    target_link = config("FRONTEND_DEPLOY_URL") + "/auth/" + payload["url_params"] + "/" + token

    await email.send_link(
        {"type": payload["link_type"], "link": target_link, "email": payload["user_email"]}
    )


def get_item_from_user_cart(req: Request, product_id: str, size: str):
    def find_item(item: cart_item_model.CartItem, id: str, size: str):
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
    if cart_item.qty >= 1 and cart_item.qty < stock:
        cart_item.qty += 1 if operation_type == OperationType.INC else -1
        db.commit()
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
def issue_coupons(user_id: str, db: Session):
    coupon_services.create_10_user_coupons(user_id, db)


def calc_cart_length(cart_id: str, db: Session):
    num_of_cart_items = (
        db.query(func.sum(cart_item_model.CartItem.qty)).filter_by(cart_id=cart_id).scalar()
    )
    return num_of_cart_items


def is_google_login(email: str, password: str):
    return True if email and not password else False


def is_email_login(email: str, password: str):
    return True if email and password else False


def create_google_login_user(user_data: user_schema.GoogleLoginUserDataSchema, db: Session):
    payload = {
        "email": user_data["email"],
        "first_name": user_data["given_name"],
        "last_name": user_data["family_name"] if "family_name" in user_data else "",
        "upload_avatar": user_data["picture"],
        "verified": True,
    }

    new_user = svc_create_user(payload, db)

    create_cart(new_user.id, db)
    issue_coupons(new_user.id, db)
    return gen_user_info_and_tokens(new_user, cart_length=0)


async def create_email_login_user(payload: user_schema.UserCreateSchema, db: Session):
    new_user = svc_create_user(payload, db)
    create_cart(new_user.id, db)
    issue_coupons(new_user.id, db)

    link_params = {
        "user_id": new_user.id,
        "user_email": new_user.email,
        "link_type": constants.URLLinkType.VERIFY,
        "token_type": constants.TokenType.VALIDATE_EMAIL,
        "url_params": constants.URLParams.VERIFY_EMAIL,
    }

    await send_link(link_params)
