from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///./courses.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()