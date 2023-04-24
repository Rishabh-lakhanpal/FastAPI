from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
app = FastAPI()


@app.get('/blog')
def index(limit = 10, published: bool =True, sort:Optional[str] = None):
    if published:
        return {'data': f'{limit} published blog'}
    else:
        return {'data': f'{limit} blog '}
    return {"data":"blog list"}

@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}

@app.get('/blog/{id}/comment')
def comment(id):
    return {'data':'comment'}

class Blog(BaseModel):
    title: str
    body :str
    published_at :Optional[bool]

@app.post('/blog')
def create_blog(request :Blog):
    return {'data':'blog is created with {request.title}'}