from pipeline.loaders.document_loader import DocumentLoader
from pipeline.processors.placement_processors import PlacementProcessor
from pipeline.embeddings.embedding_model import EmbeddingModel
from pipeline.vectorstore.chroma_store import ChromaVectorStore


def main():

    # ==========================================
    # 1. Load PDFs
    # ==========================================

    loader = DocumentLoader("data")

    documents = loader.load_documents()

    print(
        f"\nPages loaded: {len(documents)}"
    )


    
   # ==========================================
# 2. Process Placement Data
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
    # 3. Display Structured Data
    # ==========================================

    print("\n" + "=" * 70)
    print("STRUCTURED DOCUMENTS")
    print("=" * 70)

    for i, document in enumerate(
        structured_documents,
        start=1
    ):

        print(f"\nDocument {i}")
        print("-" * 70)

        print(
            document.page_content
        )


    # ==========================================
    # 4. Embedding Model
    # ==========================================

    embedding_model = EmbeddingModel()

    print(
        "\nEmbedding model initialized"
    )


    # ==========================================
    # 5. Structured ChromaDB
    # ==========================================

    chroma_store = ChromaVectorStore(
        embedding_model=embedding_model,
        persist_directory="data/chroma_db_structured"
    )

    vector_store = (
        chroma_store.get_vector_store()
    )


    # ==========================================
    # 6. Store Structured Documents
    # ==========================================

    chroma_store.add_documents(
        structured_documents
    )


    print(
        "\nStructured documents stored "
        "in ChromaDB"
    )


if __name__ == "__main__":
    main()