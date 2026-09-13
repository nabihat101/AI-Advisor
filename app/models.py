from sqlalchemy import Column, Integer, String, Text
from .database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    prerequisites = Column(Text)
    department = Column(String)
    level = Column(Integer)
    topics = Column(String)
    breadth = Column(String)
    source_url = Column(String)