from pipeline.loaders.document_loader import DocumentLoader
from pipeline.processors.academic_processor import AcademicProcessor
from pipeline.retriever.bm25_retriever import BM25Retriever


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


print("\n" + "=" * 80)
print("CREATING BM25 RETRIEVER")
print("=" * 80)

bm25 = BM25Retriever(
    documents=academic_documents,
    k=5
)

print("BM25 retriever created successfully.")


query = input("\nEnter query: ")


print("\n" + "=" * 80)
print("BM25 SEARCH RESULTS")
print("=" * 80)

results = bm25.retrieve(query)


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
    print(document.page_content[:1000])


print("\n" + "=" * 80)
print("BM25 TEST COMPLETED")
print("=" * 80)