from typing import Optional

from pydantic import BaseModel, Field, root_validator


class ProductBaseSchema(BaseModel):
    id: str
    name: str | None = Field(None, max_length=50)
    img: str | None = None
    price: float | None = Field(None, ge=0.0)

    @root_validator(pre=True)
    def check_at_least_one_attribute(cls, values):
        print(len(values),'長度')
        print(values,'全部')
        return values
    

ProductBaseSchema(name="woe",img="dd",price=39.5,id='ddfao',donotknow='dd')

#ProductBaseSchema(id='ddfao')

res = list(ProductBaseSchema.__annotations__.keys())
print(res,'annotation')


