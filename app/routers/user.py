from fastapi import FastAPI,HTTPException, Body,Header,Response,APIRouter,Depends
from enum import Enum
from pydantic import BaseModel,Field
from typing import Annotated
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from ..utils.dependencies import *

from ..schemas import user as user_schema,item as item_schema




from ..database import db,crud
from sqlalchemy.orm import Session

class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []
class SongName(str,Enum):
    idol = 'idol'
    micdrop = 'mic_drop'
    run = 'run'
items = {

    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


#--------------------router --------------
@router.post("/users/", response_model=user_schema.User)
def create_user(
    user: user_schema.UserCreate, 
    db: Session = Depends(db.get_db)
    ):
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=list[user_schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(db.get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, db: Session = Depends(db.get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}/items/", response_model=item_schema.Item)
def create_item_for_user(
    user_id: int, item: item_schema.ItemCreate, db: Session = Depends(db.get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


#-------------





@router.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item


# @router.get(
#         "/portal", 
#         response_model=None,
#         tags=["users"],
#         summary="summ: THis is so cool",
#         description="des: What is this used for??"

# )
# async def get_portal(teleport: bool = False) -> Response | dict:
#     if teleport:
#         return Response(content="123")
#     return {"message": "Here's your interdimensional portal."}


# @router.get("/items/")
# async def read_items() -> list[Item]:
#     return [
#         {"name": "Portal Gun", "price": 42.0},
#         {"name": "Plumbus", "price": 32.0},
#     ]



# @router.get("/get_header/")
# async def read_items(authorization: Annotated[str | None, Header()] = None):
#     return {"Authorization": authorization}

# @router.get("/")
# async def root():
#     return {"message": "Hello World"}

# @router.get("/get_name/{name}")
# def getName(name: SongName):
#     if name in SongName:
#         return {"song_name": SongName[name].value}
#     return HTTPException(status_code=404, detail="song not found")


# @router.put("/items/{item_id}")
# async def create_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
#     results = {"item_id": item_id, "item": item}
#     return results
