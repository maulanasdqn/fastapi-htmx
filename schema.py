from pydantic import BaseModel

class ProductBase(BaseModel):
    product_name: str
    color: str
    category: str
    price: int


class ProductCreate(ProductBase):
    pass
