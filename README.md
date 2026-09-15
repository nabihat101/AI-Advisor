# UofT AI Academic Advisor

This is an AI-powered academic planning assistant for University of Toronto Computer Science students. The application retrieves course information from the official UofT Academic Calendar, stores structured course data in SQLite, indexes course documents with ChromaDB, and uses retrieval-augmented generation (RAG) to provide grounded answers to student questions.

## Features

* Automatically collects UofT Computer Science course information from the official Academic Calendar
* Stores structured course data using SQLite and SQLAlchemy
* Uses ChromaDB for document retrieval
* Uses retrieval-augmented generation (RAG) to provide factual answers
* Handles course-specific prerequisite questions
* Provides links to official UofT course pages as sources
* FastAPI backend with a browser-based frontend
* Automated tests using pytest
## Tech 

**Backend**

* Python
* FastAPI
* SQLAlchemy
* SQLite

**AI / Retrieval**

* ChromaDB
* Retrieval-Augmented Generation (RAG)
* Groq API
* OpenAI GPT-OSS 120B

**Data Processing**

* Requests
* BeautifulSoup
* Regular Expressions

**Frontend**

* HTML
* CSS
* JavaScript

**Testing**

* pytest

## Example Questions

The advisor can answer questions such as:

* What prerequisites do I need for CSC311?
* What courses are related to artificial intelligence?
* What courses should I consider if I am interested in machine learning?
* What is CSC148 about?
* What are the prerequisites for CSC311?

For course-specific questions, the system retrieves the relevant course information before generating a response.

## Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd "AI Advisor"
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_api_key_here
```

Do not commit your `.env` file to GitHub.

### 5. Build the course database

```bash
python -m app.seed
```

### 6. Ingest UofT course information

```bash
python ingestion/ingest_courses.py
```

### 7. Build the vector index

```bash
python rag/index_courses.py
```

### 8. Start the application

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/advisor
```

## Testing

Run the automated tests with:

```bash
pytest
```

The test suite checks course retrieval and FastAPI endpoints.

## Design

The system first retrieves relevant course information from the official UofT Academic Calendar and then provides that information to the language model as context.

This helps keep the AI's responses grounded in actual course information instead of relying only on what the language model already knows. The advisor also provides links to the official UofT course pages so students can check the information themselves.

## Limitations

* The current system only includes UofT Computer Science courses.
* Course information can change, so the database needs to be updated when the UofT Academic Calendar changes.
* The advisor is meant to help students explore courses and should not replace official UofT academic advising.
* Prerequisite retrieval currently works best with course codes included in the prerequisite information.

## Future Improvements

* Add more UofT departments and programs
* Support degree requirements and program planning
* Improve prerequisite parsing for MAT, STA, and other courses
* Add personalized course recommendations based on a student's interests and completed courses
* Add timetable and course scheduling recommendations
