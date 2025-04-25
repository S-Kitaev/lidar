from sqlalchemy import Column, Integer, String
from app.db.base import Base

class User(Base):
    __tablename__ = "users"  # явно указываем имя таблицы

    user_id = Column(Integer, primary_key=True, index=True)
    user_name  = Column(String(20), nullable=False, unique=True, index=True)
    user_password = Column(String(60), nullable=False)   # длина 60 для bcrypt-хэша
    email = Column(String(50), nullable=True, unique=True, index=True)