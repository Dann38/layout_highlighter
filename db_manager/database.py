from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settingsDB
from fastapi_utils.guid_type import setup_guids_postgresql

POSTGRES_URL = f"postgresql://{settingsDB.POSTGRES_USER}:{settingsDB.POSTGRES_PASSWORD}" + \
               f"@{settingsDB.POSTGRES_HOSTNAME}:{settingsDB.DATABASE_PORT}" + \
               f"/{settingsDB.POSTGRES_DB}"

engine = create_engine(
    POSTGRES_URL, echo=True
)
setup_guids_postgresql(engine)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
