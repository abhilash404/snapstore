from typing import Annotated
from fastapi import APIRouter,Depends, HTTPException
from pydantic import BaseModel
from app.database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.models import User
from app.schemas import CreateUserRequest, Token
from passlib.context import CryptContext
from jose import jwt,JWTError


router = APIRouter(prefix='/auth',tags=['auth'])

SECRET_KEY = 'zehahaha'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# db_dependency = Annotated(Session, Depends(get_db))


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: Annotated[Session, Depends(get_db)], create_user_request: CreateUserRequest):
    create_user_model = User(
        email=create_user_request.username,
        password_hash = bcrypt_context.hash(create_user_request.password)
    )

    db.add(create_user_model)
    db.commit()

