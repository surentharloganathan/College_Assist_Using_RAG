from langchain_chroma import Chroma



class ChromaVectorStore:

    def __init__(
        self,
        embedding_model,
        persist_directory="data/chroma_db_structured",
        collection_name="college_documents_structured"
    ):

        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_model.get_model(),
            persist_directory=persist_directory
        )
    print("Connected to ChromaDB")
    def add_documents(self, documents):

        self.vector_store.add_documents(documents)
        print(f"Added{len(documents)} documents to chromaDB")

    def get_vector_store(self):

        return self.vector_store
    def similarity_search(self, query, k=5):
        return self.vector_store.similarity_search(
            query,
            k=k
        )
    def get_document_count(self):
        return self.vector_store._collection.count()