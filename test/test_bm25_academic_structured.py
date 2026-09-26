from rank_bm25 import BM25Okapi

from pipeline.loaders.document_loader import DocumentLoader
from pipeline.processors.academic_processor import AcademicProcessor


print("=" * 80)
print("LOADING DOCUMENTS")
print("=" * 80)

loader = DocumentLoader("data")
documents = loader.load_documents()


print("\n" + "=" * 80)
print("PROCESSING ACADEMIC DOCUMENTS")
print("=" * 80)

processor = AcademicProcessor()
academic_documents = processor.process(documents)

print("Total academic documents:", len(academic_documents))


# ---------------------------------------------------------
# Create a structured searchable representation
# ---------------------------------------------------------

searchable_documents = []

for document in academic_documents:

    metadata = document.metadata

    course_code = str(
        metadata.get("course_code", "")
    )

    course_name = str(
        metadata.get("course_name", "")
    )

    unit = str(
        metadata.get("unit", "")
    )

    unit_title = str(
        metadata.get("unit_title", "")
    )

    content = document.page_content

    # Important metadata is explicitly included
    searchable_text = f"""
    course_code {course_code}
    course_name {course_name}
    unit {unit}
    unit_title {unit_title}
    {course_name}
    {unit_title}
    {content}
    """

    searchable_documents.append(
        searchable_text.lower().split()
    )


print("\n" + "=" * 80)
print("CREATING STRUCTURED BM25")
print("=" * 80)

bm25 = BM25Okapi(searchable_documents)

print("Structured BM25 created successfully.")


# ---------------------------------------------------------
# Query
# ---------------------------------------------------------

query = input("\nEnter query: ")

tokenized_query = query.lower().split()

scores = bm25.get_scores(tokenized_query)

ranked_indices = sorted(
    range(len(scores)),
    key=lambda i: scores[i],
    reverse=True
)


# ---------------------------------------------------------
# Return only positive-score results
# ---------------------------------------------------------

results = []

for index in ranked_indices:

    if scores[index] <= 0:
        continue

    results.append(
        (
            academic_documents[index],
            scores[index]
        )
    )

    if len(results) >= 5:
        break


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("STRUCTURED BM25 SEARCH RESULTS")
print("=" * 80)

for i, (document, score) in enumerate(results, 1):

    print("\n" + "-" * 80)
    print("Result", i)
    print("-" * 80)

    print("BM25 Score  :", score)
    print("Course Code :", document.metadata.get("course_code"))
    print("Course Name :", document.metadata.get("course_name"))
    print("Semester    :", document.metadata.get("semester"))
    print("Credits     :", document.metadata.get("credits"))
    print("Unit        :", document.metadata.get("unit"))
    print("Unit Title  :", document.metadata.get("unit_title"))

    print("\nContent:")
    print(document.page_content[:700])


print("\n" + "=" * 80)
print("STRUCTURED BM25 TEST COMPLETED")
print("=" * 80)