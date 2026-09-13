from fastapi import FastAPI
from .database import SessionLocal
from .models import Course

app = FastAPI()


@app.get("/")
def home():
    return {"message": "UofT Course Advisor is running!"}


@app.get("/courses")
def get_courses():
    db = SessionLocal()

    courses = db.query(Course).all()

    db.close()

    return courses


@app.get("/courses/{course_code}")
def get_course(course_code: str):
    db = SessionLocal()

    course = (
        db.query(Course)
        .filter(Course.code == course_code.upper())
        .first()
    )

    db.close()

    if course is None:
        return {"error": "Course not found"}

    return course


@app.get("/search")
def search_courses(query: str):
    db = SessionLocal()

    courses = (
        db.query(Course)
        .filter(
            Course.code.contains(query.upper())
            | Course.name.contains(query)
            | Course.description.contains(query)
        )
        .all()
    )

    db.close()

    return courses