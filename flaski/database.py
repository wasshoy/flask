from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# wiki.db を作成
databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'wiki.db')
# sqlite で テーブルのCREATEを行う
engine = create_engine('sqlite:///' + databese_file, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# インスタンス作成
Base = declarative_base()
Base.query = db_session.query_property()


# Baseの内容でdb初期化
def init_db():
    import flaski.models
    Base.metadata.create_all(bind=engine)