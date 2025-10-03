from typing import Annotated
from fastapi import APIRouter,Depends, HTTPException
from app.database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.models import User
from app.schemas import CreateUserRequest, Token
from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import timedelta, datetime, timezone


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

db_dependency = Annotated[Session, Depends(get_db)]


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: Annotated[Session, Depends(get_db)], create_user_request: CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        password_hash = bcrypt_context.hash(create_user_request.password)
    )

    db.add(create_user_model)
    db.commit()

@router.post('/token', response_model= Token)
async def login_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
                      db: db_dependency):
    user= authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user.')
    
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}

def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.password_hash):
        return False
    return user


def create_access_token(username, user_id, expires_delta: timedelta):
    encode = {'sub': username, 'id':user_id}
    expires = datetime.now(timezone.utc) +expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='could not validata user.')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='could not validata user.')
