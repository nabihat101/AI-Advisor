from rag.retriever import search_documents

def test_course_lookup():
    results = search_documents("What are the prerequisites for CSC311?")
    assert len(results) > 0
    assert results[0]["metadata"]["course_code"].startswith("CSC311")

def test_general_search():
    results = search_documents(
        "I am interested in artificial intelligence and machine learning."
    )
    assert len(results) > 0