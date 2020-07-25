from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class ProductBase(BaseModel):
    code: str
    summary: str = None


class ProductCreation(ProductBase):
    ...


class ProductEdit(ProductBase):
    uuid: str


class ProductDelete(BaseModel):
    uuid: str


class Product(ProductBase):
    uuid: str
    taken: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class ProductTotal(BaseModel):
    all: int
    taken: int
    available: int


class ProductResponse(BaseModel):
    total: ProductTotal
    products: List[Product]


class ProductQuery(BaseModel):
    taken: bool = False
    desc: bool = True


class Order(BaseModel):
    mod_id: str
    mod_display_name: str
    owner_display_name: str
    uuid: str
    requested_at: datetime
    product: Product


class OrderTotal:
    total: int
    orders: List[Order]


class OrderQuery(BaseModel):
    skip: int = 0
    limit: int = 8
    moderator: str = None
    owner: str = None
    desc: bool = True


class OrderWithTotal(BaseModel):
    total: int
    orders: List[Order]
