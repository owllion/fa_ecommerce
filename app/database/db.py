from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
from decouple import config
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(config('DB_URL'))


SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)
session = SessionLocal()

Base = declarative_base()
#use to create our application’s database model
metadata = Base.metadata

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
