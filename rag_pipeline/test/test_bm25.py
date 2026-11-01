from pipeline.loaders.document_loader import DocumentLoader
from pipeline.processors.placement_processors import PlacementProcessor
from pipeline.retriever.bm25_retriever import BM25Retriever


def main():

    # ==========================================
    # 1. Load Documents
    # ==========================================

    loader = DocumentLoader("data")

    documents = loader.load_documents()

    print(
        f"\nPages loaded: {len(documents)}"
    )


    # ==========================================
    # 2. Process Placement Documents
    # ==========================================

    processor = PlacementProcessor()

    structured_documents = processor.process(
        documents
    )

    print(
        f"Structured documents created: "
        f"{len(structured_documents)}"
    )


    # ==========================================
    # 3. Create BM25 Retriever
    # ==========================================

    retriever = BM25Retriever(
        documents=structured_documents,
        k=5
    )

    print(
        "BM25 Retriever initialized"
    )


    # ==========================================
    # 4. Query
    # ==========================================

    question = (
        "What was the placement percentage "
        "of IT in 2022-2023?"
    )


    # ==========================================
    # 5. Retrieve
    # ==========================================

    results = retriever.retrieve(
        question
    )


    # ==========================================
    # 6. Display Results
    # ==========================================

    print("\n" + "=" * 70)
    print("BM25 RETRIEVER RESULTS")
    print("=" * 70)

    print(
        f"\nQuery: {question}"
    )

    print(
        f"Results: {len(results)}"
    )


    for i, (document, score) in enumerate(
        results,
        start=1
    ):

        print(
            f"\nResult {i}"
        )

        print(
            "-" * 70
        )

        print(
            "BM25 Score:",
            score
        )

        print(
            "Source:",
            document.metadata.get(
                "source"
            )
        )

        print(
            "Page:",
            document.metadata.get(
                "page"
            )
        )

        print(
            "Document Type:",
            document.metadata.get(
                "document_type"
            )
        )

        print("\nContent:")

        print(
            document.page_content
        )


if __name__ == "__main__":
    main()