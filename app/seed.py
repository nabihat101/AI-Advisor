from .database import SessionLocal, engine, Base
from .models import Course

Base.metadata.create_all(bind=engine)

db = SessionLocal()

courses = [
    Course(code="CSC311", name="Introduction to Machine Learning", description="Introduction to machine learning and statistical methods.", prerequisites="CSC207, MAT235"),
    Course(code="CSC384", name="Introduction to Artificial Intelligence", description="Introduction to artificial intelligence techniques.", prerequisites="CSC263, CSC265"),
    Course(code="CSC207", name="Software Design", description="Software development, design, testing, and object-oriented programming.", prerequisites="CSC111"),
]

db.add_all(courses)
db.commit()
db.close()