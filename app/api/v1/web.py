from pathlib import Path
from fastapi import APIRouter, Request, Depends, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from lidar.app.crud.user import get_user_by_id, get_user_by_name
from lidar.app.core.security import verify_password, create_access_token, decode_access_token
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

    # Создаем токен доступа
    token = create_access_token({"sub": str(user.user_id)})

    # Редирект на домашнюю страницу пользователя по его ID
    response = RedirectResponse(url=f"/{user.user_id}", status_code=303)
    response.set_cookie("Authorization", f"Bearer {token}", httponly=True)
    return response

@router.get("/{user_id}", response_class=HTMLResponse)
async def home(
    request: Request,
    user_id: int,
    authorization: str = Cookie(None),
    db=Depends(get_db),  # Добавляем зависимость для доступа к базе данных
    templates: Jinja2Templates = Depends(get_templates)
):
    # username = "Гость"
    # payload = None
    user = get_user_by_id(db, user_id)
    # if authorization and authorization.startswith("Bearer "):
    #     token = authorization.replace("Bearer ", "")
    #     try:
    #         payload = decode_access_token(token)
    #         if "sub" in payload:
    #             # Проверяем, что пользователь существует в базе данных
    #             user = get_user_by_id(db, payload["sub"])
    #             if user and user.user_id == user_id:
    #                 username = user.user_name  # Предполагается, что у вас есть поле username в модели пользователя
    #     except Exception as e:
    #         print(f"Ошибка декодирования токена: {e}")  # Для отладки
    return templates.TemplateResponse("main.html", {"request": request, "username": user.user_name})
