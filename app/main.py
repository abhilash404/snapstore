from fastapi import FastAPI, Depends , status , Response, HTTPException
import app.schemas as schemas, app.models as models
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session 

# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(engine)

app = FastAPI()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()



@app.get('/')
def index():
    return {'data': {'name':'sarthak','age': 40}}

@app.get('/blog/{id}',status_code=200, response_model=schemas.ShowBlog)
def get_one(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    return blog

@app.post('/blog')
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def get_blog(db: Session = Depends(get_db)):
    blog = db.query(models.Blog).all()
    return blog 

@app.delete('/blog/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete(id, db:Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id,request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="nahi degi")

    blog.update(request.dict())
    db.commit()
    return {"details": 'done'}

