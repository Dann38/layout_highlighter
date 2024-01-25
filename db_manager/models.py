from database import Base
from sqlalchemy import Column, LargeBinary, Integer, String, ForeignKey

from sqlalchemy.orm import relationship, backref


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    image64 = Column(LargeBinary, nullable=True)
    name = Column(String, nullable=True)
    segment_data = relationship("SegmentData", cascade='all, delete')
    content = relationship("Content", cascade="all, delete")

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


class Folder(Base):
    __tablename__ = "folders"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    contents = relationship("FolderContent", cascade="all, delete")
    content = relationship("Content", cascade="all, delete")

class FolderContent(Base):
    __tablename__ = "foldercontents"
    id = Column(Integer, primary_key=True)
    folder_parent_id = Column(Integer, ForeignKey("folders.id"))
    folder_parent = relationship("Folder")
    content_id = Column(Integer, ForeignKey("contents.id"))
    content = relationship("Content")

class Content(Base):
    __tablename__ = "contents"
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer,  ForeignKey('documents.id'), nullable=True)
    document = relationship("Document")  
    folder_id = Column(Integer,  ForeignKey('folders.id'), nullable=True)
    folder = relationship("Folder") 
    folder_content = relationship("FolderContent", cascade="all, delete")