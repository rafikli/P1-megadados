from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
USER = os.getenv("USER_SQL")
PASSWORD = os.getenv("PASSWORD_SQL")

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "mysql://"+USER+":"+PASSWORD+"@localhost/base_crud"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
