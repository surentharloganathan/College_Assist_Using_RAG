from pipeline.embeddings.embedding_model import EmbeddingModel
from pipeline.vectorstore.chroma_store import ChromaVectorStore


def main():

    # Create embedding model
    embedding_model = EmbeddingModel()

    # Connect to existing ChromaDB
    chroma_store = ChromaVectorStore(
        embedding_model=embedding_model
    )

    vector_store = chroma_store.get_vector_store()

    # Query
    query = "What was the placement percentage of IT?"

    # Similarity search
    results = vector_store.similarity_search(
        query,
        k=3
    )

    # Display results
    print("\n" + "=" * 70)
    print("CHROMADB RESULTS")
    print("=" * 70)

    for i, result in enumerate(results):

        print(f"\nResult {i + 1}")
        print("-" * 70)

        print("Source:", result.metadata.get("source"))
        print("Page:", result.metadata.get("page"))

        print("\nContent:")
        print(result.page_content[:500])


if __name__ == "__main__":
    main()