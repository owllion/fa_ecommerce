from fastapi import Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ...constants import api_msgs
from ...database import db
from ...exceptions.main import get_exception
from ...models.cart import cart_item_model
from ...schemas import cart_schema, user_schema
from ...services import product_services, user_services
from ...utils.depends.dependencies import *
from ...utils.router.router_settings import (
    get_path_decorator_settings,
    get_router_settings,
)
from ...utils.security.security import decode_token

_, protected_singular, _, public_singular = get_router_settings(
    singular_prefix="user", plural_prefix="users", tags=["user"]
)


@protected_singular.post(
    "/update", **get_path_decorator_settings(description="Successfully update user data")
)
def update_user(
    req: Request, payload: user_schema.UserUpdateSchema, db: Session = Depends(db.get_db)
):
    try:
        data = payload.dict(exclude_unset=True)
        user = req.state.mydata

        for field, value in data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        db.commit()

    except Exception as e:
        get_exception(e)


@protected_singular.post(
    "/reset-password",
    **get_path_decorator_settings(description="Password has been successfully reset")
)
def reset_password(payload: user_schema.ResetPasswordSchema, db: Session = Depends(db.get_db)):
    try:
        user = decode_token(payload.token, payload.token_type, db)
        user.password = payload.password
        db.commit()

    except Exception as e:
        get_exception(e)


@protected_singular.post(
    "/modify-password",
    **get_path_decorator_settings(description="Password has been successfully modified")
)
def modify_password(
    req: Request, payload: user_schema.ModifyPasswordSchema, db: Session = Depends(db.get_db)
):
    try:
        req.state.mydata.password = payload.password
        db.commit()
    except Exception as e:
        get_exception(e)


@public_singular.post(
    "/forgot-password",
    **get_path_decorator_settings(description="Password has been successfully reset")
)
async def forgot_password(payload: user_schema.EmailBaseSchema, db: Session = Depends(db.get_db)):
    try:
        user = user_services.find_user_with_email(payload.email, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist!"
            )

        link_params = {
            "user_id": user.id,
            "user_email": user.email,
            "link_type": "reset",
            "url_params": "reset-password/token",
        }

        await user_services.send_verify_or_reset_link(link_params)

        content = {
            "detail": "A verification email has been sent to your registered email address successfully."
        }
        return JSONResponse(content=content, status_code=200)

    except Exception as e:
        get_exception(e)


@protected_singular.post(
    "/upload-avatar", **get_path_decorator_settings(description="Successfully upload your avatar!")
)
def get_uploaded_avatar_url(
    req: Request, payload: user_schema.UserUploadAvatarSchema, db: Session = Depends(db.get_db)
):
    try:
        req.state.mydata.upload_avatar = payload.url
        db.commit()

    except Exception as e:
        get_exception(e)


@protected_singular.post(
    "/add-to-cart",
    **get_path_decorator_settings(description="Successfully add the product to the cart.")
)
def add_to_cart(
    req: Request, payload: cart_schema.CartItemBaseSchema, db: Session = Depends(db.get_db)
):
    try:
        user_cart = req.state.mydata.cart

        # 沒有的話，會是{}
        cart_item = user_services.get_item_from_user_cart(req, payload.product_id, payload.size)

        # 取庫存、新增cart_item使用
        product = product_services.find_product_with_id(payload.product_id, db)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=api_msgs.PRODUCT_NOT_FOUND
            )

        res = list(
            filter(
                lambda x: x.product_id == product.id and x.size.value == payload.size,
                product.product_items,
            )
        )
        stock = res[0].stock if res else None
        print(stock, "這是stock")
        print(res, "這是res")

        if cart_item:  # 如果商品存在
            is_available = cart_item.qty + payload.qty < stock
            if is_available:  # 判斷現在傳入的qty是否<庫存
                # 不用再判斷qty是否>1了 只要最後結果是<stock就可以
                cart_item.qty += payload.qty
                # 是-> 就直接加
            else:  # 不足，就說庫存不足
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=api_msgs.PRODUCT_IS_NOT_AVAILABLE_ERROR,
                )

        else:  # 商品不存在 新增一個
            # 也要先判斷數字是否<庫存
            print(payload.qty, "qty!!")
            # print(product.stock, 'stock')
            is_available = payload.qty < stock
            if is_available:
                new_cart_item = cart_item_model.CartItem(
                    qty=payload.qty, product_id=product.id, cart_id=user_cart.id, size=payload.size
                )

                db.add(new_cart_item)

                user_cart.cart_items.append(new_cart_item)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=api_msgs.PRODUCT_IS_NOT_AVAILABLE_ERROR,
                )

        db.commit()

    except Exception as e:
        get_exception(e)


@protected_singular.post(
    "/remove-from-cart",
    **get_path_decorator_settings(description="Successfully remove the product from the cart.")
)
def remove_from_cart(
    req: Request, payload: cart_schema.RemoveFromCartSchema, db: Session = Depends(db.get_db)
):
    try:
        # cart_item = user_services.get_item_from_cart_item_table(req, payload.product_id, db)
        cart_item = user_services.get_item_from_user_cart(req, payload.product_id, payload.size)

        user_services.delete_item(db, cart_item)

    except Exception as e:
        get_exception(e)


@protected_singular.post(
    "/update-cart-item-qty",
    **get_path_decorator_settings(description="Successfully update item's quantity.")
)
def update_item_qty(
    req: Request, payload: cart_schema.UpdateItemQtySchema, db: Session = Depends(db.get_db)
):
    try:
        cart_item = user_services.get_item_from_user_cart(req, payload.product_id, payload.size)

        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=api_msgs.CART_ITEM_NOT_FOUND
            )

        # 取庫存、新增cart_item使用
        product = product_services.find_product_with_id(payload.product_id, db)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=api_msgs.PRODUCT_NOT_FOUND
            )

        res = list(
            filter(
                lambda x: x.product_id == product.id and x.size.value == payload.size,
                product.product_items,
            )
        )

        stock = res[0].size.value if res else None

        print(stock, res)
        # ------

        user_services.update_qty(cart_item, stock, payload.operation_type, db)

    except Exception as e:
        get_exception(e)


@protected_singular.get(
    "/cart",
    **get_path_decorator_settings(
        description="Get user's cart", response_model=list[cart_schema.CartItemSchema]
    )
)
def get_user_cart(req: Request, db: Session = Depends(db.get_db)):
    try:
        items = jsonable_encoder(req.state.mydata.cart.cart_items)
        first_p = jsonable_encoder(req.state.mydata.cart.cart_items[0].product)
        #    print(first_p,'首個商品')
        #    print(items)
        #    print(len(req.state.mydata.cart.cart_items),"長度")
        cart_items = req.state.mydata.cart.cart_items
        for item in req.state.mydata.cart.cart_items:
            res = jsonable_encoder(item.product)
            print(res, "這是res")
            # print(jsonable_encoder(item.product))
        return [item for item in cart_items]

    except Exception as e:
        get_exception(e)


@protected_singular.get("/{user_id}", response_model=user_schema.UserSchema)
def get_user(user_id: str, db: Session = Depends(db.get_db)):
    try:
        user = user_services.find_user_with_id(user_id, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist!"
            )
        return user
    except Exception as e:
        get_exception(e)
