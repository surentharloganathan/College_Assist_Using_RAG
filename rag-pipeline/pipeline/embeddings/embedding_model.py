from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingModel:

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.model = HuggingFaceEmbeddings(
            model_name=model_name
        )
    def get_model(self):

        return self.model

    
    def embed_documents(self, documents):
        texts = [doc.page_content for doc in documents]

        return self.model.embed_documents(texts)

    def embed_query(self, query: str):
        return self.model.embed_query(query)