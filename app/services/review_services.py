from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import db
from ..models.review import review_model
from ..schemas import review_schema


def find_review_with_id(id: str, db: Session):
    review = db.query(review_model.Review).filter(review_model.Review.id == id).first()

    return review


def get_reviews(db: Session):
    reviews = db.query(review_model.Review).all()
    return reviews


def get_user_reviews(user_id: str, db: Session):
    reviews = db.query(review_model.Review).filter(review_model.Review.user_id == user_id).all()
    return reviews


def create_new_review(payload: review_schema.ReviewCreateSchema, db: Session):
    new_review = review_model.Review(**payload.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review
