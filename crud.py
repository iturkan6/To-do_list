from datetime import datetime
from typing import Union

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic.datetime_parse import timedelta
from sqlalchemy.orm import Session

import models
import schemas
from database import LocalSession

KEY = "065f9e0f7fb1901f406b192740d24a6b542c8b926ee775bcf0b3e43eed54ee0c"
ALGORITHM = "HS256"
EXPIRATION_TIME_MINUTES = 30
exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_contex = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return pwd_contex.hash(password)


def verify_password(given_password: str, db_password: str) -> bool:
    return pwd_contex.verify(given_password, db_password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_by_username(username: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    return user


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, KEY, algorithms=[ALGORITHM], options={"verify_aud": False})
        username = payload.get("sub")
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise exception
    user = db.query(models.User).filter(models.User.id == int(token_data.username)).first()
    if user is None:
        raise exception
    return user


def authenticate(db: Session, username: str, password: str):
    user = get_user_by_username(username, db)
    if not user:
        raise exception
    if not verify_password(password, user.hashed_password):
        raise exception
    return user


def create_user(db: Session, user: schemas.UserCreate):
    if get_user_by_username(user.username, db):
        raise exception
    user = models.User(name=user.name,
                       surname=user.surname,
                       username=user.username,
                       hashed_password=hash_password(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_tasks(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, KEY, algorithms=[ALGORITHM], options={"verify_aud": False})
        username = payload.get("sub")
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise exception
    tasks = db.query(models.Task).filter(models.Task.user_id == int(token_data.username)).all()
    if tasks is None:
        raise exception
    return tasks


def create_task(task: schemas.TaskCreate, db: Session, username: str):
    user = get_user_by_username(username, db)
    if not user:
        raise exception
    task_db = models.Task(**task.dict(), user_id=user.id)
    db.add(task_db)
    db.commit()
    db.refresh(task_db)
    return task_db
