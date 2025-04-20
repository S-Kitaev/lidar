from pathlib import Path

from fastapi import APIRouter, Request, Depends, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from starlette import status

from lidar.app.crud.user import get_user_by_name, get_user_by_id
from lidar.app.core.security import verify_password, create_access_token, decode_access_token
from lidar.app.db.session import get_db
from lidar.app.core.config import settings

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def get_templates():
    return templates

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

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
            "login.html",
            {"request": request, "error": "Неправильные учётные данные"}
        )

    token = create_access_token({"sub": str(user.user_id)})

    response = RedirectResponse(
        url=f"/{user.user_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {token}",
        httponly=True,
        secure=False,            # для HTTP на localhost
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/"
    )
    return response

@router.get("/{user_id}", response_class=HTMLResponse)
async def home(
    request: Request,
    user_id: int,

    authorization: str = Cookie(None, alias="Authorization"),
    db=Depends(get_db),
    templates: Jinja2Templates = Depends(get_templates)
):
    if not authorization or not authorization.startswith("Bearer "):
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_access_token(token)
    except Exception:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    if "sub" not in payload or int(payload["sub"]) != user_id:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    user = get_user_by_id(db, user_id)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "main.html",
        {"request": request, "username": user.user_name}
    )
