from pipeline.embeddings.embedding_model import EmbeddingModel
from pipeline.vectorstore.chroma_store import ChromaVectorStore
from pipeline.retriever.retriever import DocumentRetriever
from pipeline.prompts.prompt import RAGPrompt


def main():

     
    # 1. Embedding Model
     

    embedding_model = EmbeddingModel()


     
    # 2. Existing ChromaDB
     

    chroma_store = ChromaVectorStore(
        embedding_model=embedding_model
    )

    vector_store = chroma_store.get_vector_store()


     
    # 3. Retriever
     

    retriever = DocumentRetriever(
        vector_store=vector_store,
        k=3
    )


     
    # 4. Question
     

    question = "List the number of courses in the fifth semester in Department of Information Technology of Government College Of Technology?"


     
    # 5. Retrieve Documents
     

    documents = retriever.retrieve(question)

    print(f"\nDocuments retrieved: {len(documents)}")


     
    # 6. Create RAG Prompt
     

    rag_prompt = RAGPrompt()


     
    # 7. Format Retrieved Documents
     

    context = rag_prompt.format_context(documents)


     
    # 8. Create Final Prompt
     

    prompt = rag_prompt.get_prompt()

    formatted_prompt = prompt.invoke(
        {
            "context": context,
            "question": question
        }
    )


     
    # 9. Display
     

    print("\n" + "=" * 70)
    print("AUGMENTED PROMPT")
    print("=" * 70)

    print(formatted_prompt)


if __name__ == "__main__":
    main()