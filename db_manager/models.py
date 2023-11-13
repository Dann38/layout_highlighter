from database import Base
from sqlalchemy import Column, DateTime, LargeBinary, ForeignKey
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy.orm import relationship, backref


class Image(Base):
    __tablename__ = "images"
    id = Column(GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    image = Column(LargeBinary, nullable=True)
    date_create = Column(DateTime,  server_default=func.now())
    date_update = Column(DateTime, server_default=func.now(), onupdate=func.now())

    processing = relationship('Processing', backref='image')


class Processing(Base):
    __tablename__ = "processing"
    id = Column(GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    id_image = Column(GUID, ForeignKey('images.id'))
    # id_tesseract_processing = Column(GUID, ForeignKey('tesseract_processing.id'))


# class TesseractProcess(Base):
#     __tablename__ = "tesseract_processing"
#     id = Column(GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
#     bboxes = Column(LargeBinary, nullable=True)

