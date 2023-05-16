import json

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field, root_validator
from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.orm import declarative_base, joinedload, relationship, sessionmaker

from app.models.product import (
    product_image_url_model,
    product_model,
    thumbnail_url_model,
)
from app.models.review import review_model
from app.models.user import user_model

engine = create_engine('mysql+mysqldb://root:test123!!!@127.0.0.1:3306/practice_db')


Session = sessionmaker(bind=engine)
session = Session()
# Make the DeclarativeMeta
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(90), unique=True, index=True)
    hashed_password = Column(String(20),nullable=True)
    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), index=True)
    description = Column(String(80), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
Base.metadata.create_all(engine)


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass

class Owner(BaseModel):
    email: str
    id: int
class ItemSchema(ItemBase):
    id: int
    owner_id: int
    
    class Config:
        orm_mode = True
class MainItem(ItemSchema):
    owner: Owner
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    id: int
    items: list[ItemSchema] = []
    class Config:
        orm_mode = True

# user1 = User(email="abc@example.com")
# user2 = User(email="def@example.com")
# session.add(user1)
# session.add(user2)

# session.commit()
# item1 = Item(title="Title 1", description="Description 1", owner_id=user1.id)
# item2 = Item(title="Title 2", description="Description 2", owner_id=user1.id)
# item3 = Item(title="Title 3", description="Description 3", owner_id=user2.id)
# session.add(item1)
# session.add(item2)
# session.add(item3)

# session.commit()

app = FastAPI(title="Bookipedia")

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/items/", response_model=list[MainItem])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items


#-------------------------------
# class Book(Base):
#     __tablename__ = 'books'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(80), nullable=False)
#     authors = relationship("Author", secondary="book_authors", back_populates='books')

# class Author(Base):
#     __tablename__ = 'authors'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(60), nullable=False)
#     books = relationship("Book", secondary="book_authors", back_populates='authors')
# class BookAuthor(Base):
#     __tablename__ = 'book_authors'
#     book_id = Column(ForeignKey('books.id'), primary_key=True)
#     author_id = Column(ForeignKey('authors.id'), primary_key=True)
#     blurb = Column(String(500), nullable=False,default="what is blurb")
# # Create the tables in the database
# # Base.metadata.create_all(engine)

# class AuthorBase(BaseModel):
#     id: int
#     name: str

#     class Config:
#         orm_mode = True

# class BookBase(BaseModel):
#     id: int
    

#     class Config:
#         orm_mode = True

# class BookSchema(BookBase):
#     authors: list[AuthorBase]

# class AuthorSchema(AuthorBase):
#     books: list[BookBase]
# # book = session.query(Book).options(joinedload(Book.authors)).first()
# # b1_schema = BookSchema.from_orm(book)
# # print(b1_schema,'這是b1死雞馬')
# # print(book.json)


# #-------------------------------------API-
# app = FastAPI(title="Bookipedia")

# def get_db():
#     db = Session(bind=engine)
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/books/{id}", response_model=BookSchema)
# async def get_book(id: int, db: Session = Depends(get_db)):
#     db_book = db.query(Book).options(joinedload(Book.authors)).\
#         where(Book.id == id).one()
#     return db_book


