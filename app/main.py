from fastapi import FastAPI,HTTPException, Body,Header,Response,APIRouter,Depends
from enum import Enum
from pydantic import BaseModel,Field
from typing import Annotated
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from .utils.dependencies import *
app = FastAPI()
router = APIRouter()
router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
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

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}


# ----

@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item


@app.get(
        "/portal", 
        response_model=None,tags=["users"],
        summary="summ: THis is so cool",
        description="des: What is this used for??"

)
async def get_portal(teleport: bool = False ) -> Response | dict:
    if teleport:
        return Response(content="123")
    return {"message": "Here's your interdimensional portal."}


@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]



@app.get("/get_header/")
async def read_items(authorization: Annotated[str | None, Header()] = None):
    return {"Authorization": authorization}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/get_name/{name}")
def getName(name: SongName):
    if name in SongName:
        return {"song_name": SongName[name].value}
    return HTTPException(status_code=404, detail="song not found")


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
