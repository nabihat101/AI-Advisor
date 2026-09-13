import chromadb

from app.database import SessionLocal
from app.models import Course


# Connect to ChromaDB
client = chromadb.PersistentClient(path="./vector_db")

collection = client.get_or_create_collection(
    name="uoft_academic_documents"
)


def course_to_document(course):
    """
    Convert a Course database object into text
    that can be embedded and searched.
    """

    return f"""
    Course: {course.code}
    Name: {course.name}

    Department: {course.department}
    Level: {course.level}

    Description:
    {course.description}

    Prerequisites:
    {course.prerequisites}

    Topics:
    {course.topics}

    Breadth:
    {course.breadth}
    """


def index_courses():
    db = SessionLocal()

    courses = db.query(Course).all()

    for course in courses:

        document = course_to_document(course)

        collection.upsert(
            ids=[course.code],
            documents=[document],
            metadatas=[{
                "type": "course",
                "course_code": course.code,
                "course_name": course.name,
                "department": course.department,
                "level": course.level,
                "source_url": course.source_url
            }]
        )
    db.close()

    print(f"Indexed {len(courses)} courses.")


if __name__ == "__main__":
    index_courses()