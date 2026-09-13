import re
import requests
from bs4 import BeautifulSoup
from app.database import SessionLocal, Base, engine
from app.models import Course

BASE_URL = "https://artsci.calendar.utoronto.ca"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_course_links():
    links = []
    for page in range(10):
        url = BASE_URL + "/search-courses"
        params = {
            "course_keyword": "",
            "field_breadth_requirements_value": "All",
            "field_distribution_requirements_value": "All",
            "field_prerequisite_value": "",
            "field_section_value": "Computer Science",
            "page": page
        }
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if re.search(r"/course/csc\d+[hy]\d+", href, re.IGNORECASE):
                full_url = BASE_URL + href if href.startswith("/") else href
                if full_url not in links:
                    links.append(full_url)
    return links

def clean_text(text):
    return " ".join(text.split())

def extract_course(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = clean_text(soup.get_text(" ", strip=True))

    match = re.search(r"(CSC\d{3}[HY]\d?)", text)
    if not match:
        return None

    code = match.group(1)
    title = soup.find("h1")
    name = clean_text(title.get_text()) if title else code

    description = ""
    prerequisites = ""

    prereq_match = re.search(
        r"Prerequisite[s]?:\s*(.*?)(?=Exclusion[s]?:|Hours?:|$)",
        text,
        re.IGNORECASE
    )

    if prereq_match:
        prerequisites = prereq_match.group(1).strip()

    description_match = re.search(
        r"Description\s+(.*?)(?=Prerequisite[s]?:|Exclusion[s]?:|Hours?:|$)",
        text,
        re.IGNORECASE
    )

    if description_match:
        description = description_match.group(1).strip()

    return {
        "code": code,
        "name": name,
        "description": description,
        "prerequisites": prerequisites,
        "department": "Computer Science",
        "level": int(code[3:6]),
        "source_url": url
    }

def save_course(course):
    db = SessionLocal()

    existing = db.query(Course).filter(
        Course.code == course["code"]
    ).first()

    if existing:
        existing.name = course["name"]
        existing.description = course["description"]
        existing.prerequisites = course["prerequisites"]
        existing.department = course["department"]
        existing.level = course["level"]
        existing.source_url = course["source_url"]
    else:
        db.add(Course(
            code=course["code"],
            name=course["name"],
            description=course["description"],
            prerequisites=course["prerequisites"],
            department=course["department"],
            level=course["level"],
            source_url=course["source_url"]
        ))

    db.commit()
    db.close()

def main():
    Base.metadata.create_all(bind=engine)
    links = get_course_links()
    print(f"Found {len(links)} CSC course pages.")
    saved = 0
    for url in links:
        try:
            course = extract_course(url)
            if course:
                save_course(course)
                saved += 1
                print(f"✓ Saved {course['code']} - {course['name']}")
        except requests.RequestException as error:
            print(f"Failed: {url}")
            print(error)
    print(f"\nSaved {saved} courses to SQLite.")

if __name__ == "__main__":
    main()