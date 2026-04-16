from typing import Optional
from sqlmodel import Field,SQLModel

class User(SQLModel,table = True):
    __tablename__ = 'users'

    id :Optional[int] = Field(default=None, primary_key=True)
    name:str 
    email:Optional[str] = Field(index=True,unique=True)
    is_active:bool = True