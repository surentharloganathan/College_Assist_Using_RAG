# from pipeline.embeddings.embedding_model import EmbeddingModel
# from pipeline.vectorstore.chroma_store import ChromaVectorStore
# from pipeline.retriever.retriever import DocumentRetriever


# def main():

#         # 1. Create Embedding Model
    
#     embedding_model = EmbeddingModel()

#     print("Embedding model initialized")


#         # 2. Connect to Existing ChromaDB
    
#     chroma_store = ChromaVectorStore(
#         embedding_model=embedding_model
#     )

#     vector_store = chroma_store.get_vector_store()

#     print("Connected to ChromaDB")


#         # 3. Create Retriever
    
#     retriever = DocumentRetriever(
#         vector_store=vector_store,
#         k=3
#     )

#     print("Retriever initialized")


#         # 4. Query
#     question = "What was the placement percentage of IT?"

#         # 5. Retrieve Documents
    
#     results = retriever.retrieve(question)


#         # 6. Display Results
    
#     print("\n" + "=" * 70)
#     print("RETRIEVER RESULTS")
#     print("=" * 70)

#     print(f"\nQuery: {question}")
#     print(f"Documents retrieved: {len(results)}")


#     for i, document in enumerate(results):

#         print(f"\nResult {i + 1}")
#         print("-" * 70)

#         print("Source:")
#         print(document.metadata.get("source"))

#         print("\nPage:")
#         print(document.metadata.get("page"))

#         print("\nContent:")
#         print(document.page_content[:500])



# if __name__ == "__main__":

#     main()



from pipeline.embeddings.embedding_model import EmbeddingModel
from pipeline.vectorstore.chroma_store import ChromaVectorStore

def main():

    # ==========================================
    # 1. Embedding Model
    # ==========================================

    embedding_model = EmbeddingModel()


    # ==========================================
    # 2. ChromaDB
    # ==========================================

    chroma_store = ChromaVectorStore(
        embedding_model=embedding_model
    )

    vector_store = chroma_store.get_vector_store()


    # ==========================================
    # 3. Query
    # ==========================================

    question = "What was the placement percentage of IT in 2022-2023?"

    # ==========================================
    # 4. Similarity Search With Scores
    # ==========================================

    results = vector_store.similarity_search_with_score(
        question,
        k=20
    )


    # ==========================================
    # 5. Display
    # ==========================================

    print("\n" + "=" * 70)
    print("SIMILARITY SEARCH WITH SCORES")
    print("=" * 70)

    print(f"\nQuery: {question}")
    print(f"Results: {len(results)}")


    for i, (document, score) in enumerate(results):

        print(f"\nResult {i + 1}")
        print("-" * 70)

        print("Score:", score)

        print("Source:",
              document.metadata.get("source"))

        print("Page:",
              document.metadata.get("page"))

        print("\nContent:")
        print(document.page_content[:500])


if __name__ == "__main__":
    main()
