from sqlalchemy import create_engine
# from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from decouple import config
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(config('DB_URL'))
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)
# autocommit=False, autoflush=False,
session = SessionLocal()

Base = declarative_base()
#use to create our application’s database model,

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
