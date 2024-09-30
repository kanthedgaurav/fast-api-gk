from apps.v1 import route_blog, route_login
from fastapi import APIRouter

app_router = APIRouter()

app_router.include_router(route_blog.router, tags=[""], prefix="", include_in_schema=False)
app_router.include_router(route_login.router, tags=[""], prefix="/auth", include_in_schema=False)