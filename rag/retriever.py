import re
import chromadb

client = chromadb.PersistentClient(path="./vector_db")

collection = client.get_collection(
    name="uoft_academic_documents"
)

def search_documents(query, n_results=3):
    course_match = re.search(r"\bCSC\d{3}\b", query.upper())

    if course_match:
        course_code = course_match.group(0)
        all_courses = collection.get()

        for document, metadata in zip(
            all_courses["documents"],
            all_courses["metadatas"]
        ):
            stored_code = metadata["course_code"].upper()

            if stored_code.startswith(course_code):
                results = [{
                    "document": document,
                    "metadata": metadata,
                    "distance": 0.0
                }]

                prerequisite_match = re.search(
                    r"Prerequisites?:\s*(.*?)(?:\n\n|$)",
                    document,
                    re.IGNORECASE | re.DOTALL
                )

                if prerequisite_match:
                    prerequisite_text = prerequisite_match.group(1)

                    prerequisite_codes = re.findall(
                        r"\bCSC\d{3}\b",
                        prerequisite_text.upper()
                    )

                    for prereq_code in prerequisite_codes:
                        for prereq_doc, prereq_metadata in zip(
                            all_courses["documents"],
                            all_courses["metadatas"]
                        ):
                            if prereq_metadata["course_code"].upper().startswith(prereq_code):
                                results.append({
                                    "document": prereq_doc,
                                    "metadata": prereq_metadata,
                                    "distance": 0.0
                                })
                                break

                return results

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return [
        {
            "document": document,
            "metadata": metadata,
            "distance": distance
        }
        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )
    ]