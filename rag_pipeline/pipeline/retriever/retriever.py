from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever


class DocumentRetriever:

    def __init__(
        self,
        vector_store,
        k: int = 3 
    ):

        self.retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": k,
                "fetch_k": 10
            }
)

    def retrieve(
        self,
        query: str
    ) -> list[Document]:

        return self.retriever.invoke(query)