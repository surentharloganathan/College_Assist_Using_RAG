from pipeline.vectorstore.chroma_store import ChromaVectorStore
from pipeline.embeddings.embedding_model import EmbeddingModel
from pipeline.retriever.bm25_retriever import BM25Retriever
from pipeline.retriever.hybridretriever import HybridRetriever
from pipeline.loaders.document_loader import DocumentLoader
from pipeline.processors.placement_processors import PlacementProcessor
from pipeline.rag.rag_pipeline import RAGPipeline


def main():

    print("\n" + "=" * 70)
    print("RAG PIPELINE TEST")
    print("=" * 70)

    # 1. Load documents
    loader = DocumentLoader("data")
    documents = loader.load_documents()

    # 2. Process placement documents
    processor = PlacementProcessor()
    placement_documents = processor.process(documents)

    # 3. Load embedding model
    embedding_model = EmbeddingModel()

    # 4. Connect to existing Chroma database
    chroma_store = ChromaVectorStore(
        embedding_model=embedding_model,
        persist_directory="data/chroma_db",
        collection_name="placement_statistics"
    )

    vector_store = chroma_store.get_vector_store()

    # 5. Create BM25 retriever
    bm25 = BM25Retriever(
        placement_documents,
        k=20
    )

    # 6. Create Hybrid Retriever
    hybrid_retriever = HybridRetriever(
        vector_store=vector_store,
        bm25_retriever=bm25,
        k=5,
        fetch_k=20
    )

    # 7. Create RAG Pipeline
    rag = RAGPipeline(hybrid_retriever)

    # 8. Ask question
    question = "What was the placement percentage of IT in 2022-2023?"

    print("\nQuestion:")
    print(question)

    answer = rag.ask(question)

    # 9. Display answer
    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)
    print(answer)


if __name__ == "__main__":
    main()