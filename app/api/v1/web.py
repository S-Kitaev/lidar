from pathlib import Path
from fastapi import APIRouter, Request, Depends, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt

from lidar.app.crud.user import get_user_by_name
from lidar.app.core.security import verify_password, create_access_token
from lidar.app.db.session import get_db
from lidar.app.core.config import settings

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def get_templates():
    return templates

@router.get("/login", response_class=HTMLResponse)
async def login_form(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates)
):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@router.post("/login", response_class=HTMLResponse)
async def login_web(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db),
    templates: Jinja2Templates = Depends(get_templates)
):
    user = get_user_by_name(db, username)
    if not user or not verify_password(password, user.user_password):
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "Неправильные учётные данные"}
        )
    token = create_access_token({"sub": str(user.user_id)})
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie("Authorization", f"Bearer {token}", httponly=True)
    return response

@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    authorization: str = Cookie(None),
    templates: Jinja2Templates = Depends(get_templates)
):
    username = "Гость"
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
        try:
            payload = jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=[settings.ALGORITHM])
            username = payload.get("sub")
        except JWTError:
            pass
    return templates.TemplateResponse("welcome.html", {"request": request, "username": username})
