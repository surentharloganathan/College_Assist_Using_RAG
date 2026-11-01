from pipeline.vectorstore.chroma_store import ChromaVectorStore
from pipeline.processors.academic_processor import AcademicProcessor
from pipeline.embeddings.embedding_model import EmbeddingModel
from pipeline.loaders.document_loader import DocumentLoader
from pipeline.retriever.bm25_retriever import BM25Retriever
from pipeline.retriever.hybridretriever import HybridRetriever


def main():

    print("\n" + "=" * 70)
    print("HYBRID RETRIEVER - ACADEMIC TEST")
    print("=" * 70)


    # ============================================================
    # 1. Load Academic PDF
    # ============================================================

    print("\n>>> Loading academic PDF...")

    loader = DocumentLoader("data")

    documents = loader.load_documents()

    print(
        f">>> Loaded {len(documents)} pages"
    )


    # ============================================================
    # 2. Process Academic Documents
    # ============================================================

    print("\n>>> Processing academic documents...")

    processor = AcademicProcessor()

    academic_documents = processor.process(
        documents
    )

    print(
        f">>> Academic documents created: "
        f"{len(academic_documents)}"
    )


    # ============================================================
    # 3. Initialize Embedding Model
    # ============================================================

    print("\n>>> Loading embedding model...")

    embedding_model = EmbeddingModel()

    # Get the actual embedding model
    embedding_function = embedding_model.get_model()


    # ============================================================
    # 4. Connect to Existing Academic ChromaDB
    # ============================================================

    print("\n>>> Connecting to Academic ChromaDB...")

    vector_store = ChromaVectorStore(
        embedding_model=embedding_model,
        persist_directory="data/chroma_db_academic",
        collection_name="academic_courses"
    )

    print(
        ">>> Academic ChromaDB connected"
    )


    # ============================================================
    # IMPORTANT:
    # DO NOT call add_documents()
    #
    # The Academic ChromaDB already contains 466 documents.
    # ============================================================


    # ============================================================
    # 5. Create Structured BM25
    # ============================================================

    print("\n>>> Creating BM25 Retriever...")

    bm25_retriever = BM25Retriever(
        academic_documents,
        k=20
    )

    print(
        ">>> BM25 Retriever created"
    )


    # ============================================================
    # 6. Create Hybrid Retriever
    # ============================================================

    print("\n>>> Creating Hybrid Retriever...")

    hybrid_retriever = HybridRetriever(
        vector_store=vector_store,
        bm25_retriever=bm25_retriever,
        k=5,
        fetch_k=20,
        rrf_constant=60
    )

    print(
        ">>> Hybrid Retriever created"
    )


    # ============================================================
    # 7. Test Queries
    # ============================================================

    queries = [

        "Computer Networks Unit III",

        "22IPC509 Unit III",

        "IPv4 IPv6 Subnetting"

    ]


    # ============================================================
    # 8. Run Hybrid Retrieval
    # ============================================================

    for query in queries:

        print("\n\n")

        print(
            "#" * 70
        )

        print(
            f"QUERY: {query}"
        )

        print(
            "#" * 70
        )


        results = hybrid_retriever.retrieve(
            query
        )


        # ========================================================
        # Display Final Results
        # ========================================================

        print("\n")

        print(
            "=" * 70
        )

        print(
            "FINAL HYBRID RESULTS"
        )

        print(
            "=" * 70
        )


        for i, document in enumerate(
            results,
            start=1
        ):

            metadata = document.metadata


            print(
                f"\nResult {i}"
            )

            print(
                "-" * 50
            )


            print(
                "Course Code:",
                metadata.get(
                    "course_code",
                    "N/A"
                )
            )


            print(
                "Course Name:",
                metadata.get(
                    "course_name",
                    "N/A"
                )
            )


            print(
                "Semester:",
                metadata.get(
                    "semester",
                    "N/A"
                )
            )


            print(
                "Unit:",
                metadata.get(
                    "unit",
                    "N/A"
                )
            )


            print(
                "Unit Title:",
                metadata.get(
                    "unit_title",
                    "N/A"
                )
            )


            print(
                "Source:",
                metadata.get(
                    "source",
                    "N/A"
                )
            )


            print(
                "Page:",
                metadata.get(
                    "page",
                    "N/A"
                )
            )


            print(
                "Content:"
            )

            print(
                document.page_content[:500]
            )


    print("\n")
    print("=" * 70)
    print("ACADEMIC HYBRID TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()