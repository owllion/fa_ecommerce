from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from decouple import config
from sqlalchemy.ext.declarative import declarative_base

url = URL.create(
    drivername= "mysql",
    username= config('DB_USER'),
    password= config('DB_PASSWORD'),
    host= config('DB_HOST'),
    database= config('DB_NAME'),
    port= config('DB_PORT')
)

engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)
# autocommit=False, autoflush=False,
session = SessionLocal()

Base = declarative_base()