from fastapi import FastAPI
from .app.api.v1 import auth
from .app.db.base import Base
from .app.db.session import engine

# При разработке: автоматически создаём таблицы (в продакшене — через миграции Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="IoT Platform API")

# Регистрируем роутеры
app.include_router(auth.router)
