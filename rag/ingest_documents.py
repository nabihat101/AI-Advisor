import chromadb


# Create a persistent local vector database
client = chromadb.PersistentClient(path="./vector_db")


# Create a collection for academic documents
collection = client.get_or_create_collection(
    name="uoft_academic_documents"
)


documents = [
    {
        "id": "csc311",
        "text": """
        CSC311 Introduction to Machine Learning.

        This course introduces machine learning and statistical
        methods for learning from data.

        Prerequisites: CSC207 and the required mathematics and
        statistics preparation.

        Topics include machine learning, statistical methods,
        prediction, classification, and learning from data.
        """,
        "metadata": {
            "type": "course",
            "course_code": "CSC311",
            "department": "CSC"
        }
    },

    {
        "id": "csc384",
        "text": """
        CSC384 Introduction to Artificial Intelligence.

        This course introduces techniques and methods in
        artificial intelligence.

        Topics include artificial intelligence, search,
        reasoning, and computational problem solving.

        Prerequisites include the required computer science
        preparation.
        """,
        "metadata": {
            "type": "course",
            "course_code": "CSC384",
            "department": "CSC"
        }
    },

    {
        "id": "csc207",
        "text": """
        CSC207 Software Design.

        This course focuses on software development, software
        design, testing, and object-oriented programming.

        Prerequisite: CSC111.

        The course develops software engineering skills that
        are useful for later computer science courses.
        """,
        "metadata": {
            "type": "course",
            "course_code": "CSC207",
            "department": "CSC"
        }
    },

    {
        "id": "csc343",
        "text": """
        CSC343 Introduction to Databases.

        This course introduces database systems, relational
        models, SQL, and database design.

        Prerequisite: CSC207.

        Topics include databases, SQL, relational data,
        and data management.
        """,
        "metadata": {
            "type": "course",
            "course_code": "CSC343",
            "department": "CSC"
        }
    }
]


collection.add(
    ids=[document["id"] for document in documents],
    documents=[document["text"] for document in documents],
    metadatas=[document["metadata"] for document in documents]
)


print(f"Added {len(documents)} documents to the vector database.")