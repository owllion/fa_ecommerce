from fastapi import Depends, HTTPException, status

from ...constants import api_msgs
from ...exceptions.main import get_exception, raise_http_exception
from ...schemas import review_schema
from ...services import review_services
from ...utils.depends.dependencies import *
from ...utils.router.router_settings import (
    get_path_decorator_settings,
    get_router_settings,
)

protected_plural, protected_singular, public_plural, public_singular = get_router_settings(
    singular_prefix="review", plural_prefix="reviews", tags=["review"]
)


@protected_singular.post(
    "/",
    **get_path_decorator_settings(
        description="Successfully create a review of the product.",
        response_model=review_schema.ReviewSchema,
    )
)
def create_review(payload: review_schema.ReviewCreateSchema, db: Session = Depends(db.get_db)):
    try:
        new_product = review_services.svc_create_review(payload, db)

        return new_product

    except Exception as e:
        get_exception(e)


@public_singular.get(
    "/{review_id}",
    **get_path_decorator_settings(
        description="Get the data of a single review.", response_model=review_schema.ReviewSchema
    )
)
def get_review(review_id: str, db: Session = Depends(db.get_db)):
    try:
        review = review_services.find_review_with_id(review_id, db)

        if not review:
            raise_http_exception(api_msgs.REVIEW_NOT_FOUND)

        return review

    except Exception as e:
        get_exception(e)


@public_plural.get(
    "/",
    **get_path_decorator_settings(
        description="Get the review list", response_model=list[review_schema.ReviewSchema]
    )
)
def get_reviews(db: Session = Depends(db.get_db)):
    try:
        reviews = review_services.svc_get_reviews(db)

        return reviews

    except Exception as e:
        get_exception(e)


@public_plural.get(
    "/user/{user_id}",
    **get_path_decorator_settings(
        description="Get the specific user's review list",
        response_model=list[review_schema.ReviewSchema],
    )
)
def get_user_reviews(user_id: str, db: Session = Depends(db.get_db)):
    try:
        client = req.app.state.redis

        cached_orders = client.json().get(user_orders_key(user_id), ".")

        total_len = client.json().arrlen(user_orders_key(user_id), ".")

        if cached_orders and total_len:
            return {"list": cached_orders, "total": total_len}

        # orders = order_services.get_orders_by_user_id(user_id, db)
        orders = req.state.mydata.orders

        json_orders = list(map(lambda x: jsonable_encoder(x), orders))

        client.json().set(user_orders_key(user_id), ".", json_orders)

        client.expire(user_orders_key(user_id), timedelta(seconds=60))

        total_len = client.json().arrlen(user_orders_key(user_id), ".")

        return {"list": orders, "total": total_len}
        # reviews = review_services.svc_get_user_reviews(user_id, db)

        # return reviews

    except Exception as e:
        get_exception(e)


@protected_singular.put(
    "/",
    **get_path_decorator_settings(
        description="Successfully update the review.",
    )
)
def update_review(payload: review_schema.ReviewUpdateSchema, db: Session = Depends(db.get_db)):
    try:
        review = review_services.find_review_with_id(payload.id, db)

        if not review:
            raise_http_exception(api_msgs.REVIEW_NOT_FOUND)

        data = payload.dict(exclude_unset=True)

        for field, value in data.items():
            if hasattr(review, field):
                setattr(review, field, value)

        db.commit()

    except Exception as e:
        get_exception(e)


@protected_singular.delete(
    "/{review_id}",
    **get_path_decorator_settings(
        description="Successfully delete the review.",
    )
)
def delete_review(review_id: str, db: Session = Depends(db.get_db)):
    try:
        review = review_services.find_review_with_id(review_id, db)

        if not review:
            raise_http_exception(api_msgs.REVIEW_NOT_FOUND)

        db.delete(review)
        db.commit()

    except Exception as e:
        get_exception(e)
