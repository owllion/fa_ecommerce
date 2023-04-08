from pydantic import BaseModel, Field, validator


class Example(BaseModel):
    x: int = Field(ge=0)

    @validator('x')
    def check_x(cls, v):
        print('check_xwwwwww')
        return v

    @validator('x')
    def double_x(cls, v):
        print('double_x')
        return v * 2
Example(x=-1)