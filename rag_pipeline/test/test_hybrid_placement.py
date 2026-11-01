from pipeline.vectorstore.chroma_store import ChromaVectorStore
from pipeline.processors.placement_processors import PlacementProcessor
from pipeline.embeddings.embedding_model import EmbeddingModel
from pipeline.loaders.document_loader import DocumentLoader
from pipeline.retriever.bm25_retriever import BM25Retriever
from pipeline.retriever.hybridretriever import HybridRetriever


def main():

    print("\n" + "=" * 70)
    print("HYBRID RETRIEVER - PLACEMENT TEST")
    print("=" * 70)


    # ============================================================
    # 1. Load Placement PDFs
    # ============================================================

    print("\n>>> Loading placement PDFs...")

    loader = DocumentLoader("data")

    documents = loader.load_documents()

    print(
        f">>> Loaded {len(documents)} pages"
    )


    # ============================================================
    # 2. Process Placement Documents
    # ============================================================

    print("\n>>> Processing placement documents...")

    processor = PlacementProcessor()

    placement_documents = processor.process(
        documents
    )

    print(
        f">>> Placement documents created: "
        f"{len(placement_documents)}"
    )


    # ============================================================
    # 3. Initialize Embedding Model
    # ============================================================

    print("\n>>> Loading embedding model...")

    embedding_model = EmbeddingModel()


    # ============================================================
    # 4. Connect to Existing Placement ChromaDB
    # ============================================================

    print("\n>>> Connecting to Placement ChromaDB...")

    vector_store = ChromaVectorStore(
        embedding_model=embedding_model,
        persist_directory="data/chroma_db",
        collection_name="placement_statistics"
    )

    print(
        ">>> Placement ChromaDB connected"
    )


    # ============================================================
    # IMPORTANT:
    # Do NOT add documents here.
    #
    # Placement ChromaDB already contains the processed
    # placement documents.
    # ============================================================


    # ============================================================
    # 5. Create BM25 Retriever
    # ============================================================

    print("\n>>> Creating BM25 Retriever...")

    bm25_retriever = BM25Retriever(
        placement_documents,
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
    # 7. Placement Queries
    # ============================================================

    queries = [

        "What was the placement percentage of IT in 2022-2023?",

        "What was the average salary for IT students in 2022-2023?",

        "What was the highest package for IT in 2023-2024?",

        "How many IT students were placed in 2023-2024?"

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
            "FINAL PLACEMENT HYBRID RESULTS"
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
                "Document Type:",
                metadata.get(
                    "document_type",
                    "N/A"
                )
            )


            print(
                "Academic Year:",
                metadata.get(
                    "academic_year",
                    "N/A"
                )
            )


            print(
                "Department:",
                metadata.get(
                    "department",
                    "N/A"
                )
            )


            print(
                "Content:"
            )

            print(
                document.page_content[:700]
            )


    print("\n")

    print(
        "=" * 70
    )

    print(
        "PLACEMENT HYBRID TEST COMPLETED"
    )

    print(
        "=" * 70
    )


if __name__ == "__main__":
    main()