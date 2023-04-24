from fastapi import APIRouter, Depends , status ,Response ,HTTPException
from ..schemas import User as UserSchema
from ..schemas import ShowUser

from sqlalchemy.orm import Session
from .. import database, models
from ..hashing import Hash

router = APIRouter(
    prefix="/user",
    tags=['User']
)


@router.post('/')
def create_user(user_field: UserSchema,db:Session = Depends(database.get_db)):
    # hashedPassword = pwd_context.hash(user_field.password)
    new_user = models.User(name=user_field.name,email=user_field.email,password=Hash.bcrypt(user_field.password))
    # new_user = models.User(**user_field.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=ShowUser)
def get_user(id:int, db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with the id {id} not found")
    return user
