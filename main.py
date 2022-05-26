from fastapi import Depends, status, FastAPI, Body
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.datetime_parse import timedelta
from sqlalchemy.orm import Session

import crud
import examples
import models
import schemas
from crud import get_db
from database import engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get("/user/", tags=["User"], response_model=schemas.User)
def get_user(current_user: schemas.User = Depends(crud.get_current_user)):
    user = current_user
    return user


@app.post("/user/signup", tags=["User"], response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(db: Session = Depends(crud.get_db),
                user: schemas.UserCreate = Body(examples=examples.example_user)):
    user = crud.create_user(db, user)
    return user


@app.post("/token", tags=["User"])
def read_users(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(form_data.username, db)
    access_token_expires = timedelta(minutes=crud.EXPIRATION_TIME_MINUTES)
    access_token = crud.create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/task", tags=["Tasks"])
def get_tasks(current_tasks: list[schemas.Task] = Depends(crud.get_tasks)):
    tasks = current_tasks
    return tasks


@app.post("/task", tags=["Tasks"], response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, username: str, db: Session = Depends(get_db)):
    task = crud.create_task(task, db, username)
    return task
