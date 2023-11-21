from database import Base
from sqlalchemy import Column, DateTime, LargeBinary, ForeignKey, Integer, JSON, String
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
    segments = relationship("Segment", back_populates="image")


class Processing(Base):
    __tablename__ = "processing"
    id = Column(GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    id_image = Column(GUID, ForeignKey('images.id'))
    date_create = Column(DateTime, server_default=func.now())
    date_update = Column(DateTime, server_default=func.now(), onupdate=func.now())
    # id_tesseract_processing = Column(GUID, ForeignKey('tesseract_processing.id'))


# class TesseractProcess(Base):
#     __tablename__ = "tesseract_processing"
#     id = Column(GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
#     bboxes = Column(LargeBinary, nullable=True)

class Label(Base):
    __tablename__ = "labels"
    id = Column(Integer, primary_key=True)
    name = Column(String(125), nullable=False)

    segments = relationship("Segment", back_populates="label")


class Segment(Base):
    __tablename__ = "segments"
    id = Column(GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    segment = Column(LargeBinary, nullable=True)
    image_id = Column(GUID, ForeignKey('images.id'))
    x0 = Column(Integer, nullable=True)
    y0 = Column(Integer, nullable=True)
    x1 = Column(Integer, nullable=True)
    y1 = Column(Integer, nullable=True)
    graph = Column(JSON, nullable=True)
    label_id = Column(Integer, ForeignKey('labels.id'))

    image = relationship("Image", back_populates="segments")
    label = relationship("Label", back_populates="segments")
