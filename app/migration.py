from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from database import db
from models import item_model,user_model
from alembic import command
# 創建一個 session
Session = sessionmaker(bind=db.engine)
session = Session()

# 刪除參照該表格的其他表格，或解除參照關係
try:
    session.query(item_model.Item).delete()
    session.commit()
except IntegrityError:
    session.rollback()

# 刪除該表格
db.Base.metadata.tables['user'].drop(bind=db.engine)

# 執行 alembic migration
command.revision(
    autogenerate=True,
    message='drop user table'
)
command.upgrade(
    revision='head'
)






