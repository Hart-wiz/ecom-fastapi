from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True) # unique=True prevents duplicate emails
    password: str # This will store the HASH, not the real password
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)