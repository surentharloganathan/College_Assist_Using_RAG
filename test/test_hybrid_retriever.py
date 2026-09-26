from pipeline.loaders.document_loader import DocumentLoader
from pipeline.splitter.text_splitter import DocumentSplitter

from pipeline.embeddings.embedding_model import EmbeddingModel
from pipeline.vectorstore.chroma_store import ChromaVectorStore

from pipeline.retriever.bm25_retriever import BM25Retriever
from pipeline.retriever.hybridretriever import HybridRetriever


def main():

    # ==========================================
    # 1. Load Documents
    # ==========================================

    loader = DocumentLoader("data")

    documents = loader.load_documents()

    print(f"\nPages loaded: {len(documents)}")


    # ==========================================
    # 2. Split Documents
    # ==========================================

    splitter = DocumentSplitter()

    chunks = splitter.split_documents(documents)

    print(f"Chunks created: {len(chunks)}")


    # ==========================================
    # 3. Embedding Model
    # ==========================================

    embedding_model = EmbeddingModel()

    print("Embedding model initialized")


    # ==========================================
    # 4. ChromaDB
    # ==========================================

    chroma_store = ChromaVectorStore(
        embedding_model=embedding_model
    )

    vector_store = chroma_store.get_vector_store()

    print("Connected to ChromaDB")


    # ==========================================
    # 5. BM25
    # ==========================================

    bm25_retriever = BM25Retriever(
        documents=chunks,
        k=20
    )

    print("BM25 Retriever initialized")


    # ==========================================
    # 6. Hybrid Retriever
    # ==========================================

    hybrid_retriever = HybridRetriever(
        vector_store=vector_store,
        bm25_retriever=bm25_retriever,
        k=5,
        fetch_k=20,
        rrf_constant=60
    )

    print("Hybrid Retriever initialized")


    # ==========================================
    # 7. Query
    # ==========================================

    question = (
        "What was the placement percentage "
        "of IT in 2022-2023?"
    )


    # ==========================================
    # 8. Retrieve
    # ==========================================

    results = hybrid_retriever.retrieve(
        question
    )


    # ==========================================
    # 9. Final Results
    # ==========================================

    print("\n" + "=" * 70)
    print("HYBRID RETRIEVER RESULTS")
    print("=" * 70)

    print(f"\nQuery: {question}")
    print(f"Results: {len(results)}")


    for i, document in enumerate(
        results,
        start=1
    ):

        print(f"\nResult {i}")
        print("-" * 70)

        print(
            "Source:",
            document.metadata.get("source")
        )

        print(
            "Page:",
            document.metadata.get("page")
        )

        print("\nContent:")

        print(
            document.page_content[:1000]
        )


if __name__ == "__main__":
    main()