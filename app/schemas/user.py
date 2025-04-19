from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    user_name: str
    password: str
    email: EmailStr | None = None

class UserRead(BaseModel):
    user_id: int
    user_name: str
    email: EmailStr | None

    class Config:
        orm_mode = True