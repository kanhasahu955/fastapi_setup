from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.services.user_service import UserService
from app.schemas.user_schema import CreateUser,UpdateUser,ReadUser

router = APIRouter()

def get_user_service(db: AsyncSession = Depends(get_session)) -> UserService:
    return UserService.get_users(db)

@router.post("", response_model=ReadUser)
async def create_user(payload: CreateUser,service: UserService = Depends(get_user_service)):
    return await service.create_user(payload)

@router.get("", response_model=list[ReadUser])
async def get_users(service: UserService = Depends(get_user_service)):
    return await service.get_users()

@router.get("/{user_id}", response_model=list[ReadUser])
async def get_user(user_id: int,service: UserService = Depends(get_user_service)):
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.put("/{user_id}", response_model=ReadUser)
async def update_user(user_id: int,payload: UpdateUser,service: UserService = Depends(get_user_service)):
    user = await service.update_user(user_id,payload)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int,service: UserService = Depends(get_user_service)):
    deleted = await service.delete_user(user_id)
    if not deleted:
        raise HTTPException(404, "User not found")
    return {"message": "deleted"}