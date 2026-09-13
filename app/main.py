from fastapi import FastAPI
from pydantic import BaseModel

from .database import SessionLocal
from .models import Course

from rag.retriever import search_documents
from rag.generator import generate_answer

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request


app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)

class QuestionRequest(BaseModel):
    question: str


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

@app.get("/advisor")
def advisor_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )

@app.get("/search")
def search_courses(query: str):
    db = SessionLocal()

    courses = (
        db.query(Course)
        .filter(
            Course.code.contains(query.upper())
            | Course.name.contains(query)
            | Course.description.contains(query)
            | Course.topics.contains(query)
        )
        .all()
    )

    db.close()

    return courses


@app.post("/ask")
def ask_advisor(request: QuestionRequest):

    results = search_documents(
        request.question,
        n_results=5
    )

    answer = generate_answer(
        request.question,
        results
    )

    sources = []

    for result in results:
        sources.append({
            "course_code": result["metadata"]["course_code"],
            "course_name": result["metadata"].get("course_name", ""),
            "source_url": result["metadata"].get("source_url", ""),
            "distance": result["distance"]
        })

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }