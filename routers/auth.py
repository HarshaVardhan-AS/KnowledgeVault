from fastapi import APIRouter, Depends, HTTPException, Depends
from schemas import Register
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models
from utils import password_hash
from sqlalchemy import or_
from utils import create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = "HS256"
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
@router.post("/register")
def register(register: Register, db: Annotated[Session, Depends(get_db)]):
    res = db.execute(
    select(models.User).where(or_(models.User.username == register.username, models.User.email == register.email)))
    existing_user = res.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_pw = password_hash.hash(register.password)
    new_user = models.User(
        username=register.username,
        email=register.email,
        hashed_password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User Successfully registered"}

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    res = db.execute(select(models.User).where(models.User.username == form_data.username))
    existing_user = res.scalars().first()
    if existing_user:
        if password_hash.verify(form_data.password, existing_user.hashed_password):
            token = create_access_token(existing_user.id)
            return {
                "access_token": token,
                "token_type": "bearer"
            }
    raise HTTPException(status_code=401, detail="Unauthorized")

def get_current_user(db: Annotated[Session, Depends(get_db)], token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,JWT_SECRET , algorithms = [ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    res = db.execute(select(models.User).where(models.User.id == user_id))
    user = res.scalars().first()
    #print(payload)
    #print(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user
