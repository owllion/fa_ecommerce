import pymysql
import sqlalchemy
from decouple import config
from google.cloud.sql.connector import Connector
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_name = config("DB_NAME")
db_user = config("DB_USER")
db_password = config("DB_PASSWORD")
db_host = config("DB_HOST")
db_port = config("DB_PORT")

db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# initialize Connector object
connector = Connector()


# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "fastapi-ec-387409:us-central1:faecommercedb",
        "pymysql",
        user=db_user,
        password=db_password,
        db=db_name,
    )
    return conn


# engine = create_engine(db_url)
engine = create_engine("mysql+pymysql://", creator=getconn)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()
metadata = Base.metadata


# for Depends()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
