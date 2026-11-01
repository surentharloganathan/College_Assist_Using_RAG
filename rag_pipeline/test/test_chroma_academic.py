from pipeline.embeddings.embedding_model import EmbeddingModel
from pipeline.vectorstore.chroma_store import ChromaVectorStore


print("=" * 80)
print("LOADING EMBEDDING MODEL")
print("=" * 80)

embedding_model = EmbeddingModel()


print("\n" + "=" * 80)
print("CONNECTING TO ACADEMIC CHROMADB")
print("=" * 80)

vector_store = ChromaVectorStore(
    embedding_model=embedding_model,
    persist_directory="data/chroma_db_academic",
    collection_name="academic_courses"
)

print(
    "Documents in ChromaDB:",
    vector_store.get_document_count()
)


# ============================================================
# TEMPORARY TEST
# ============================================================

print("\n" + "=" * 80)
print("TEMPORARY METADATA TEST")
print("=" * 80)

results = vector_store.vector_store.get(
    where={"course_code": "22IPC509"}
)

print("Documents found:", len(results["documents"]))

for i, content in enumerate(results["documents"]):

    metadata = results["metadatas"][i]

    print("\n" + "-" * 80)
    print("Result", i + 1)
    print("-" * 80)

    print("Course Code :", metadata.get("course_code"))
    print("Course Name :", metadata.get("course_name"))
    print("Semester    :", metadata.get("semester"))
    print("Credits     :", metadata.get("credits"))
    print("Unit        :", metadata.get("unit"))
    print("Unit Title  :", metadata.get("unit_title"))

    print("\nContent:")
    print(content[:1000])


print("\n" + "=" * 80)
print("TEMPORARY TEST COMPLETED")
print("=" * 80)