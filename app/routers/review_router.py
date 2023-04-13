from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from ..constants import api_msgs, exceptions
from ..exceptions.http_exception import CustomHTTPException
from ..schemas import review_schema
from ..services import review_services
from ..utils.dependencies import *
from ..utils.router_settings import get_path_decorator_settings, get_router_settings
from .api_router_settings import *

# protected_router = APIRouter(**get_router_settings(
#   {
#     'is_protected': True,
#     'prefix': '/review',
#     'tags': ['review'],
#     'responses': api_msgs.API_RESPONSES
#   }  
# ))

# public_router = APIRouter(**get_router_settings(
#   {
#     'is_protected': False,
#     'prefix': '/review',
#     'tags': ['review'],
#     'responses': api_msgs.API_RESPONSES
#   }  
# ))

@protected_singular.post(
    "/", 
    **get_path_decorator_settings(
        description= "Successfully create a review of the product.",
        response_model= review_schema.ReviewSchema
    )
)
def create_review(payload: review_schema.ReviewCreateSchema, db: Session = Depends(db.get_db)):
    
    try:
        new_product = review_services.save_to_db_then_return(payload,db)
        
        return new_product


    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))


@public_singular.get(
    "/{review_id}",
    **get_path_decorator_settings(
        description= "Get the data of a single review.",
        response_model= review_schema.ReviewSchema
    )
)
def get_review(review_id: str,db:Session = Depends(db.get_db)):
    try:
        review = review_services.find_review_with_id(review_id,db)

        if not review: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.REVIEW_NOT_FOUND
            )
        
        return review
          
    except Exception as e:
        if isinstance(e, exceptions.HTTPException): raise e
        raise CustomHTTPException(detail= str(e))
    
@public_plural.get(
    "/",
    **get_path_decorator_settings(
        description= "Get the review list",
        response_model= list[review_schema.ReviewSchema]
    )
)
def get_reviews(db:Session = Depends(db.get_db)):
    try:
        reviews = review_services.get_reviews(db)

        return reviews
          
    except Exception as e:
        if isinstance(e, exceptions.HTTPException): raise e
        raise CustomHTTPException(detail= str(e))
    


@public_plural.get(
    "/user/{user_id}",
    **get_path_decorator_settings(
        description= "Get the specific user's review list",
        response_model= list[review_schema.ReviewSchema]
    )
)
def get_user_reviews(user_id: str,db:Session = Depends(db.get_db)):
    try:
        reviews = review_services.get_user_reviews(user_id,db)

        return reviews
          
    except Exception as e:
        if isinstance(e, exceptions.HTTPException): raise e
        raise CustomHTTPException(detail= str(e))


@protected_singular.put(
    "/",
    **get_path_decorator_settings(
        description= "Successfully update the review.",
    )
)
def update_review(
    payload: review_schema.ReviewUpdateSchema,
    db:Session = Depends(db.get_db)
):
    try:
        review = review_services.find_review_with_id(payload.id,db)

        if not review: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.REVIEW_NOT_FOUND
            )
        
        data = payload.dict(exclude_unset=True)

        for field, value in data.items():
          if hasattr(review, field) :
              setattr(review, field, value)
        
        db.commit()
        
    except Exception as e:
        if type(e).__name__ == exceptions.HTTPException: raise e
        raise CustomHTTPException(detail= str(e))


@protected_singular.delete(
    "/{review_id}",
    **get_path_decorator_settings(
        description= "Successfully delete the review.",
    )
)
def delete_review(review_id: str,db:Session = Depends(db.get_db)):
    try:
        review = review_services.find_review_with_id(review_id,db)

        if not review: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.REVIEW_NOT_FOUND
            )
        
        db.delete(review)
        
        db.commit()
        
    except Exception as e:
        if type(e).__name__ == exceptions.HTTPException: raise e
        raise CustomHTTPException(detail= str(e))


