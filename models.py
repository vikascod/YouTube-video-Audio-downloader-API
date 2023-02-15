from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
from datetime import datetime
from database import Base


class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    file = Column(LargeBinary)
    title = Column(String)
    author = Column(String)
    length = Column(Integer)
    filesize = Column(Integer)
    filename = Column(String)


class Audio(Base):
    __tablename__ = "audios"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    file = Column(LargeBinary)
    title = Column(String)
    author = Column(String)
    length = Column(Integer)
    filesize = Column(Integer)
    filename = Column(String)