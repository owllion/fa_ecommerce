from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from decouple import config

url = URL.create(
    username= config('DB_USER'),
    password= config('DB_PASSWORD'),
    host= config('DB_HOST'),
    database= config('DB_NAME'),
    port= config('DB_PORT')
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()