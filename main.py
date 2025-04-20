from pathlib import Path
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from lidar.app.api.v1.web import router as web_router
from lidar.app.db.base import Base
from lidar.app.db.session import engine

# Авто‑создаём таблицы (только для разработки)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lidar API")

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

# Шаблоны
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.include_router(web_router)