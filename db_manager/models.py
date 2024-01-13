from database import Base
from sqlalchemy import Column, LargeBinary, Integer, String

from sqlalchemy.orm import relationship, backref


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    image64 = Column(LargeBinary, nullable=True)
    name = Column(String, nullable=True)


class Processing(Base):
    __tablename__ = "processings"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    json_processing = Column(String, nullable=True)


class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    discription = Column(String, nullable=True)
