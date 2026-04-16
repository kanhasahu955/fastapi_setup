from typing import Optional
from sqlmodel import SQLModel

class CreateUser(SQLModel):
    name:str
    email:str

class UpdateUser(SQLModel):
    name:Optional[str] = None
    email:Optional[str] = None

class ReadUser(SQLModel):
    id:int
    name:str
    email:str
    is_active:bool