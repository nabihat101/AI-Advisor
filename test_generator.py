from rag.retriever import search_documents
from rag.generator import generate_answer


question = "What prerequisites do I need for CSC311?"


results = search_documents(
    question,
    n_results=3
)


answer = generate_answer(
    question,
    results
)


print("\n" + "=" * 60)
print("AI ADVISOR")
print("=" * 60)
print(answer)