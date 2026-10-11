from pipeline.vectorstore.chroma_store import ChromaVectorStore
from pipeline.embeddings.embedding_model import EmbeddingModel


def main():

    print("\n" + "=" * 70)
    print("PLACEMENT CHROMA RETRIEVAL TEST")
    print("=" * 70)

    embedding_model = EmbeddingModel()

    vector_store = ChromaVectorStore(
        embedding_model=embedding_model,
        persist_directory="data/chroma_db",
        collection_name="placement_statistics"
    )

    print(
        "\nDocuments in Chroma:",
        vector_store.get_document_count()
    )

    queries = [
        "What was the placement percentage of IT in 2022-2023?",
        "What was the average salary for IT students in 2022-2023?",
        "What was the highest package for IT in 2023-2024?",
        "How many IT students were placed in 2023-2024?"
    ]

    for query in queries:

        print("\n" + "#" * 70)
        print("QUERY:", query)
        print("#" * 70)

        results = vector_store.similarity_search(
            query,
            k=5
        )

        print(
            f"\nChroma returned {len(results)} documents"
        )

        for i, document in enumerate(results, start=1):

            metadata = document.metadata

            print("\n" + "-" * 60)
            print(f"Result {i}")
            print("-" * 60)

            print(
                "Academic Year:",
                metadata.get("academic_year", "N/A")
            )

            print(
                "Branch:",
                metadata.get("branch", "N/A")
            )

            print(
                "Document Type:",
                metadata.get("document_type", "N/A")
            )

            print("\nContent:")
            print(document.page_content)


if __name__ == "__main__":
    main()