from pipeline.vectorstore.chroma_store import ChromaVectorStore
from pipeline.embeddings.embedding_model import EmbeddingModel
from pipeline.retriever.bm25_retriever import BM25Retriever
from pipeline.retriever.hybridretriever import HybridRetriever
from pipeline.loaders.document_loader import DocumentLoader
from pipeline.processors.placement_processors import PlacementProcessor
from pipeline.processors.academic_processor import AcademicProcessor
from pipeline.rag.rag_router import RAGRouter


def main():

    print("\n" + "=" * 70)
    print("RAG ROUTER TEST")
    print("=" * 70)

    # --------------------------------------------------
    # 1. Load all documents
    # --------------------------------------------------

    loader = DocumentLoader("data")
    documents = loader.load_documents()

    # --------------------------------------------------
    # 2. Process Placement Documents
    # --------------------------------------------------

    placement_processor = PlacementProcessor()
    placement_documents = placement_processor.process(documents)

    # --------------------------------------------------
    # 3. Process Academic Documents
    # --------------------------------------------------

    academic_processor = AcademicProcessor()
    academic_documents = academic_processor.process(documents)

    # --------------------------------------------------
    # 4. Load Embedding Model
    # --------------------------------------------------

    embedding_model = EmbeddingModel()

    # --------------------------------------------------
    # 5. Connect to Placement Chroma
    # --------------------------------------------------

    placement_chroma = ChromaVectorStore(
        embedding_model=embedding_model,
        persist_directory="data/chroma_db",
        collection_name="placement_statistics"
    )

    placement_vector_store = placement_chroma.get_vector_store()

    # --------------------------------------------------
    # 6. Connect to Academic Chroma
    # --------------------------------------------------

    academic_chroma = ChromaVectorStore(
        embedding_model=embedding_model,
        persist_directory="data/chroma_db_academic",
        collection_name="academic_courses"
    )

    academic_vector_store = academic_chroma.get_vector_store()

    # --------------------------------------------------
    # 7. Create Placement BM25
    # --------------------------------------------------

    placement_bm25 = BM25Retriever(
        placement_documents,
        k=20
    )

    # --------------------------------------------------
    # 8. Create Academic BM25
    # --------------------------------------------------

    academic_bm25 = BM25Retriever(
        academic_documents,
        k=20
    )

    # --------------------------------------------------
    # 9. Create Placement Hybrid Retriever
    # --------------------------------------------------

    placement_retriever = HybridRetriever(
        vector_store=placement_vector_store,
        bm25_retriever=placement_bm25,
        k=5,
        fetch_k=20
    )

    # --------------------------------------------------
    # 10. Create Academic Hybrid Retriever
    # --------------------------------------------------

    academic_retriever = HybridRetriever(
        vector_store=academic_vector_store,
        bm25_retriever=academic_bm25,
        k=5,
        fetch_k=20
    )

    # --------------------------------------------------
    # 11. Create RAG Router
    # --------------------------------------------------

    router = RAGRouter(
        academic_retriever=academic_retriever,
        placement_retriever=placement_retriever
    )

    # --------------------------------------------------
    # 12. Test Placement Question
    # --------------------------------------------------

    placement_question = (
        "What was the placement percentage of IT in 2022-2023?"
    )

    print("\n" + "=" * 70)
    print("TEST 1 - PLACEMENT")
    print("=" * 70)

    print("\nQuestion:")
    print(placement_question)

    placement_answer = router.route(placement_question)

    print("\nFinal Answer:")
    print(placement_answer)

    # --------------------------------------------------
    # 13. Test Academic Question
    # --------------------------------------------------

    academic_question = (
        "What topics are covered in Unit III of Cloud Computing?"
    )

    print("\n" + "=" * 70)
    print("TEST 2 - ACADEMIC")
    print("=" * 70)

    print("\nQuestion:")
    print(academic_question)

    academic_answer = router.route(academic_question)

    print("\nFinal Answer:")
    print(academic_answer)

    # --------------------------------------------------
    # 14. Test Completed
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("RAG ROUTER TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()