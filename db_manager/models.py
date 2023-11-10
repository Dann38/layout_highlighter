from database import Base
from sqlalchemy import Column, DateTime, LargeBinary
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL


class Image(Base):
    __tablename__ = "images"
    id = Column(GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    image = Column(LargeBinary, nullable=True)
    date_create = Column(DateTime,  server_default=func.now())
    date_update = Column(DateTime, server_default=func.now(), onupdate=func.now())


