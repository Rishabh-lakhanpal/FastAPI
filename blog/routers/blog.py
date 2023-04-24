from fastapi import APIRouter, Depends, status, HTTPException, Response ,Path
from .. import schemas
from typing import List 
from .. import database, models
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/blog",   
    tags=['Blog']
)

@router.get('/')
def get_blogs(db:Session = Depends(database.get_db),current_user: schemas.User = Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(blog_field : schemas.Blog, db : Session = Depends(database.get_db),current_user: schemas.User = Depends(get_current_user)):
    new_blog = models.Blog(**blog_field.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(database.get_db),current_user: schemas.User = Depends(get_current_user)):
    # destroy = db.query(models.Blog).filter(models.Blog.id== id).delete(synchronize_session=False)
    destroy = db.query(models.Blog).get(id)
    db.delete(destroy)
    db.commit()
    return "Record deleted sucessfully"


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, blog_field: schemas.Blog, db: Session = Depends(database.get_db),current_user: schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} id not found")
    blog.update(blog_field)
    db.commit()
    return 'updated'
# @router.put('/id', status_code=status.HTTP_202_ACCEPTED)
# def update(id:str,blog_field: schemas.Blog,db: Session = Depends(database.get_db),current_user: schemas.User = Depends(get_current_user)):
#     update_blog = jsonable_encoder(blog_field)
#     blog_field[id] = update_blog
#     return update_blog


@router.get('/{id}', status_code=200)
# def get_blog(id :int ,response:Response, db: Session = Depends(database.get_db),current_user: schemas.User = Depends(get_current_user)):
def get_blog(id :int = Path(description="The ID if the item You'd like to get"), db: Session = Depends(database.get_db),current_user: schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).get(id)
    # blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} id not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'Blog with the id {id} is not available'}
    return blog

