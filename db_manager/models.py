from database import Base
from sqlalchemy import Column, LargeBinary, Integer, String, ForeignKey

from sqlalchemy.orm import relationship, backref


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    image64 = Column(LargeBinary, nullable=True)
    name = Column(String, nullable=True)
    segment_data = relationship("SegmentData", cascade='all, delete')


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
    markings = relationship("MarkingSegment", cascade='all, delete')


class MarkingSegment(Base):
    __tablename__ = "markingsegments"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    dataset_id = Column(Integer, ForeignKey('datasets.id'))
    # Не обязательно для связи, но позволяет упростить запросы
    dataset = relationship("Dataset")
    segment_data = relationship("SegmentData", cascade='all, delete')


class SegmentData(Base):
    __tablename__ = "segmentdatas"
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer,  ForeignKey('documents.id'))
    document = relationship("Document")
    marking_id = Column(Integer, ForeignKey('markingsegments.id'))
    marking = relationship("MarkingSegment")
    json_data = Column(String, nullable=True)
