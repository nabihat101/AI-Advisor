from rag.retriever import search_documents


query = "I want to study artificial intelligence and machine learning."


results = search_documents(query)


print(f"\nQuery: {query}\n")


for result in results:

    print("=" * 60)

    print(
        f"Course: "
        f"{result['metadata']['course_code']}"
    )

    print(
        f"Distance: "
        f"{result['distance']:.4f}"
    )

    print(result["document"])