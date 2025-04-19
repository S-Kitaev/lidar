from pathlib import Path
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates

from lidar.app.api.v1.auth import router as auth_router
from lidar.app.api.v1.web import router as web_router
from lidar.app.db.base import Base
from lidar.app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="IoT Platform API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ✅ Указываем правильный путь до templates (где login.html реально лежит)
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# 👉 Зависимость, которую можно переиспользовать
def get_templates():
    return templates

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(title=app.title, version="1.0.0", routes=app.routes)
    components = schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})
    security_schemes["bearerAuth"] = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}

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

# Роуты
app.include_router(auth_router)
app.include_router(web_router)