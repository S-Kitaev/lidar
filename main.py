from pathlib import Path

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# from lidar.app.api.v1.auth import router as auth_router
from lidar.app.api.v1.web import router as web_router
from lidar.app.db.base import Base
from lidar.app.db.session import engine
from lidar.app.core.config import settings

# Авто‑создаём таблицы (только для разработки)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="IoT Platform API")

# CORS: разрешаем обращения с локальных портов
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Шаблоны
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def get_templates():
    return templates

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(title=app.title, version="1.0.0", routes=app.routes)
    comp = schema.setdefault("components", {})
    sec = comp.setdefault("securitySchemes", {})
    sec["bearerAuth"] = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}

    for route in app.routes:
        path = route.path
        if path in ("/auth/login", "/auth/register"):
            continue
        if path in schema.get("paths", {}):
            for method in schema["paths"][path]:
                schema["paths"][path][method].setdefault("security", []).append({"bearerAuth": []})
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi

# Роутеры
# app.include_router(auth_router)
app.include_router(web_router)