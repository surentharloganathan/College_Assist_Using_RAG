from pipeline.loaders.document_loader import DocumentLoader
from pipeline.splitter.text_splitter import DocumentSplitter
from pipeline.embeddings.embedding_model import EmbeddingModel


def main():

    # Load
    loader = DocumentLoader("data")
    documents = loader.load_documents()

    # Split
    splitter = DocumentSplitter()
    chunks = splitter.split_documents(documents)

    # Embedding model
    embedding_model = EmbeddingModel()

    # Embed one chunk
    vector = embedding_model.embed_documents(
        [chunks[0]]
    )[0]

    print("\nEmbedding created!")

    print("Vector dimensions:", len(vector))

    print("\nFirst 10 values:")
    print(vector[:10])


if __name__ == "__main__":
    main()