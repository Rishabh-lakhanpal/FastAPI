from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..hashing import Hash
from datetime import datetime, timedelta
from ..token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(login_fields: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == login_fields.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    if not Hash.verify(user.password,login_fields.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")

    access_token = create_access_token(data={"sub":user.email})
      
    return {"access_token":access_token, "token_type":"bearer"}