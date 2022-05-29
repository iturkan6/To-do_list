from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection configurations

URL = "sqlite:///./todo_list.db"

engine = create_engine(url=URL, connect_args={"check_same_thread": False})

LocalSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
