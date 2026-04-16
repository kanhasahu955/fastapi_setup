from fastapi import APIRouter

from app.api.v1.user_endpoints import router as user_router

router = APIRouter

router.include_router(user_router,prefix='/users',tags=['Users'])