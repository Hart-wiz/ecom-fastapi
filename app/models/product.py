from sqlmodel import SQLModel, Field
from typing import Optional

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    image_url: Optional[str] = None
    stock: int = Field(default=0)
    is_active: bool = Field(default=True)