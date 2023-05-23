from decouple import config
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_name = config("DB_NAME")
db_user = config("DB_USER")
db_password = config("DB_PASSWORD")
# db_host = config("DB_HOST")
db_port = config("DB_PORT")
unix_socket_path = config("UNIX_SOCKET_PATH")
cloud_sql_instance_name = config("CLOUD_SQL_INSTANCE_NAME")

# db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

db_url = f"mysql+pymysql://{db_user}:{db_password}@/{db_name}?unix_socket={unix_socket_path}/{cloud_sql_instance_name}"

engine = create_engine(db_url)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()
# use to create our application’s database model
metadata = Base.metadata


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
