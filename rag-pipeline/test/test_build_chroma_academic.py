from pipeline.loaders.document_loader import DocumentLoader
from pipeline.processors.academic_processor import AcademicProcessor
from pipeline.embeddings.embedding_model import EmbeddingModel
from pipeline.vectorstore.chroma_store import ChromaVectorStore


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
print("LOADING EMBEDDING MODEL")
print("=" * 80)

embedding_model = EmbeddingModel()


print("\n" + "=" * 80)
print("CREATING ACADEMIC CHROMADB")
print("=" * 80)

vector_store = ChromaVectorStore(
    embedding_model=embedding_model,
    persist_directory="data/chroma_db_academic",
    collection_name="academic_courses"
)


print("\nAdding academic documents to ChromaDB...")

vector_store.add_documents(academic_documents)

print("\nAcademic ChromaDB creation completed.")
print("Documents in ChromaDB:",
      vector_store.get_document_count())