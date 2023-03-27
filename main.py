from fastapi import FastAPI,HTTPException, Body
from enum import Enum
from pydantic import BaseModel,Field
from typing import Annotated

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
class SongName(str,Enum):
    idol = 'idol'
    micdrop = 'mic_drop'
    run = 'run'

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
