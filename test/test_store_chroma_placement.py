from pipeline.vectorstore.chroma_store import ChromaVectorStore
from pipeline.processors.placement_processors import PlacementProcessor
from pipeline.embeddings.embedding_model import EmbeddingModel
from pipeline.loaders.document_loader import DocumentLoader


def main():

    print("\n" + "=" * 70)
    print("STORING PLACEMENT DOCUMENTS IN CHROMA")
    print("=" * 70)

    # ------------------------------------------------------------
    # 1. Load documents
    # ------------------------------------------------------------

    print("\n>>> Loading documents...")

    loader = DocumentLoader("data")
    documents = loader.load_documents()

    print(f">>> Loaded {len(documents)} pages")


    # ------------------------------------------------------------
    # 2. Process placement documents
    # ------------------------------------------------------------

    print("\n>>> Processing placement documents...")

    processor = PlacementProcessor()

    placement_documents = processor.process(documents)

    print(
        f">>> Created {len(placement_documents)} placement documents"
    )


    # ------------------------------------------------------------
    # 3. Load embedding model
    # ------------------------------------------------------------

    print("\n>>> Loading embedding model...")

    embedding_model = EmbeddingModel()


    # ------------------------------------------------------------
    # 4. Connect to placement Chroma collection
    # ------------------------------------------------------------

    print("\n>>> Connecting to placement Chroma...")

    vector_store = ChromaVectorStore(
        embedding_model=embedding_model,
        persist_directory="data/chroma_db",
        collection_name="placement_statistics"
    )


    # ------------------------------------------------------------
    # 5. Check current count
    # ------------------------------------------------------------

    before_count = vector_store.get_document_count()

    print(
        f">>> Documents currently in Chroma: {before_count}"
    )


    # ------------------------------------------------------------
    # 6. Add placement documents
    # ------------------------------------------------------------

    if before_count == 0:

        print("\n>>> Adding placement documents...")

        vector_store.add_documents(
            placement_documents
        )

        print(">>> Placement documents added successfully.")

    else:

        print(
            "\n>>> Chroma already contains documents."
        )

        print(
            ">>> Skipping insertion to avoid duplicates."
        )


    # ------------------------------------------------------------
    # 7. Verify
    # ------------------------------------------------------------

    after_count = vector_store.get_document_count()

    print(
        f"\n>>> Documents in Chroma after operation: "
        f"{after_count}"
    )


    print("\n" + "=" * 70)
    print("PLACEMENT CHROMA STORAGE TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()