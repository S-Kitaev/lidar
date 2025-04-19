# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from fastapi.security import OAuth2PasswordRequestForm
# from lidar.app.schemas.user import UserCreate, UserRead
# from lidar.app.schemas.token import Token
# from lidar.app.crud.user import get_user_by_name, create_user
# from lidar.app.core.security import verify_password, create_access_token
# from lidar.app.db.session import get_db
#
# router = APIRouter(prefix="/auth", tags=["auth"])
#
# @router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
# def register(user_in: UserCreate, db: Session = Depends(get_db)):
#     if get_user_by_name(db, user_in.email):
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return create_user(db, user_in)
#
# @router.post("/login", response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     # если логин по имени:
#     user = get_user_by_name(db, form_data.username)
#     # либо по email:
#     # user = get_user_by_email(db, form_data.username)
#
#     if not user or not verify_password(form_data.password, user.user_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     token = create_access_token({"sub": str(user.user_id)})
#     return {"access_token": token, "token_type": "bearer"}