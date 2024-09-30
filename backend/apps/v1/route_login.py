import json 

from fastapi import APIRouter,Request , Depends
from fastapi.templating import Jinja2Templates
from fastapi import responses, status, Form
from sqlalchemy.orm import session

from db.session import get_db
from schemas.user import UserCreate
from db.repository.user import create_new_user
from apis.v1.route_login import authenticate_user
from core.security import create_access_token


templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/register")
def resgister(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@router.post("/register")
def resgister(request: Request,  email: str = Form(...), password: str = Form(...), db: session = Depends(get_db)):
    errors = []
    try:
        user = UserCreate( email=email, password=password)
        create_new_user(user, db)
        return responses.RedirectResponse(url="/?alert=Successfully%20Registered", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        erros_list = json.loads(e.json())
        for item in erros_list:
            errors.append(item.get("loc")[0] +": "+ item.get("msg"))
        return templates.TemplateResponse("auth/register.html", {"request": request, "errors": errors, "email": email})
    
@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), db: session = Depends(get_db)):
    errors = []
    user = authenticate_user(email=email, password=password, db=db)
    if not user:
        errors.append("Incorrect Email or Password")
        return templates.TemplateResponse("auth/login.html", {"request": request, "errors": errors, "email": email})
    access_token = create_access_token(data={"sub": email})
    response = responses.RedirectResponse(url="/?alert=Successfully%20Logged%20In", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}")
    return response