from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.user_model import User
from app.schemas.user_schema import CreateUser,ReadUser,UpdateUser

class UserService:
    def __init__(self,db:AsyncSession):
        self.db = db

    async def create_user(self,payload:CreateUser)->User:
        user = User(**payload.model_dump())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_users(self)->List[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()
    
    async def get_user(self,user_id:int)->Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none

    async def update_user(self,user_id:int,payload:UpdateUser)->User:
        user = await self.get_user(user_id)
        if not user:
            return None
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def delete_user(self,user_id:int)->bool:
        user = await self.get_user(user_id)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True