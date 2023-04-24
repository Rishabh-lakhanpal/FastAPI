from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHAMY_DATABASE_URL = 'sqlite:///./blog.db'   # the name of database we created

engine = create_engine(SQLALCHAMY_DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()     # use this in sqlAlchemy models that will intereact with database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close