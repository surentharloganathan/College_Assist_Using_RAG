from pipeline.loaders.document_loader import DocumentLoader
from pipeline.splitter.text_splitter import DocumentSplitter
from pipeline.embeddings.embedding_model import EmbeddingModel
from pipeline.vectorstore.chroma_store import ChromaVectorStore


def main():

    # 1. Load documents
    loader = DocumentLoader("data")
    documents = loader.load_documents()

    print(f"Pages Loaded: {len(documents)}")


    # 2. Split documents
    splitter = DocumentSplitter()
    chunks = splitter.split_documents(documents)

    print(f"Chunks Created: {len(chunks)}")


    # 3. Create embedding model
    embedding_model = EmbeddingModel()

    print("Embedding Model Initialized")


    # 4. Create ChromaDB
    chroma_store = ChromaVectorStore(
        embedding_model=embedding_model
    )

    print("ChromaDB Initialized")


    # 5. Store documents
    # Run this ONLY when ingesting new documents.
    #
    # chroma_store.add_documents(chunks)
    #
    # print("Data Stored in ChromaDB")


if __name__ == "__main__":
    main()