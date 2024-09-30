from apps.v1 import route_blog
from fastapi import APIRouter

app_router = APIRouter()

app_router.include_router(route_blog.router, tags=[""], prefix="", include_in_schema=False)