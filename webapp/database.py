from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

if os.getenv("DB_USER") and os.getenv("DB_PASSWORD") and os.getenv("DB_HOST") and os.getenv("DB_PORT") and os.getenv("DB_NAME") and os.getenv("DB_SCHEMA"):
    SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
else:
    raise ValueError("database credentains must be set")
engine = None

def database_connection():
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL, 
            connect_args={'options': '-csearch_path={}'.format(os.getenv("DB_SCHEMA"))})
        connection = engine.connect()
        connection.close()
        return True
    except Exception as e:
        print(str(e))
        return False
    

def get_db():

    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL, 
            connect_args={'options': '-csearch_path={}'.format(os.getenv("DB_SCHEMA"))})
        SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)
        db = SessionLocal()
        yield db
    finally:
        db.close()