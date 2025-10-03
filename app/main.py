from fastapi import FastAPI, Depends , status , Response, HTTPException
import app.schemas as schemas, app.models as models
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session 
from app import auth
from app.auth import get_current_user
from typing import Annotated

# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(auth.router)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]



@app.get('/', status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    return {'user': user}

@app.get('/users', status_code=200)
def get_users(response: Response, db: Session = Depends(get_db)):
    us = db.query(models.User).all()
    return us

@app.post('/new_user')
def create(request: schemas.CreateUserRequest, db: Session = Depends(get_db)):
    new_user = models.User(username=request.username, password_hash = request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



