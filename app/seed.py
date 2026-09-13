from .database import SessionLocal, engine, Base
from .models import Course


Base.metadata.create_all(bind=engine)

db = SessionLocal()


courses = [
    Course(
        code="CSC111",
        name="Foundations of Computer Science II",
        description="Introduction to programming and computational problem solving.",
        prerequisites="",
        department="CSC",
        level=100,
        topics="programming, algorithms, problem solving",
        breadth=""
    ),

    Course(
        code="CSC207",
        name="Software Design",
        description="Software development, design, testing, and object-oriented programming.",
        prerequisites="CSC111",
        department="CSC",
        level=200,
        topics="software engineering, object-oriented programming, testing",
        breadth=""
    ),

    Course(
        code="CSC311",
        name="Introduction to Machine Learning",
        description="Introduction to machine learning and statistical methods.",
        prerequisites="CSC207, MAT235",
        department="CSC",
        level=300,
        topics="machine learning, artificial intelligence, statistics",
        breadth=""
    ),

    Course(
        code="CSC384",
        name="Introduction to Artificial Intelligence",
        description="Introduction to artificial intelligence techniques.",
        prerequisites="CSC263, CSC265",
        department="CSC",
        level=300,
        topics="artificial intelligence, search, reasoning",
        breadth=""
    ),

    Course(
        code="CSC343",
        name="Introduction to Databases",
        description="Introduction to database systems, relational models, SQL, and database design.",
        prerequisites="CSC207",
        department="CSC",
        level=300,
        topics="databases, SQL, data management",
        breadth=""
    ),

    Course(
        code="CSC309",
        name="Programming on the Web",
        description="Design and implementation of web applications and web-based software.",
        prerequisites="CSC207",
        department="CSC",
        level=300,
        topics="web development, software engineering, HTTP",
        breadth=""
    ),
]


db.add_all(courses)
db.commit()
db.close()