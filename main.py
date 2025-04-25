from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.exception_handlers import http_exception_handler as default_http_handler
from app.api.v1.web  import router as web_router
from app.db.base import Base
from app.db.session import engine

# Авто‑создаём таблицы (только для разработки)
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Lidar API")
app.mount("/static", StaticFiles(directory="templates"), name="static")

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

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "templates")),
    name="static"
)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(str(BASE_DIR / "templates/images/logo.png"))

@app.exception_handler(HTTPException)
async def auth_http_exception_handler(request: Request, exc: HTTPException):
    # если это наша 401-ка, редиректим на /login
    if exc.status_code == 401:
        return RedirectResponse(url="/login", status_code=303)
    # иначе стандартный обработчик
    return await default_http_handler(request, exc)

app.include_router(web_router)