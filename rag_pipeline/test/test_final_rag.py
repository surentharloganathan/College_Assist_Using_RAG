from pipeline.vectorstore.chroma_store import ChromaVectorStore
from pipeline.embeddings.embedding_model import EmbeddingModel

from pipeline.retriever.bm25_retriever import BM25Retriever
from pipeline.retriever.hybridretriever import HybridRetriever

from pipeline.processors.contextformatter import ContextFormatter
from pipeline.prompts.prompt import RAGPrompt
from pipeline.llm.local_llm import LocalLLM

from pipeline.loaders.document_loader import DocumentLoader
from pipeline.processors.placement_processors import PlacementProcessor
from pipeline.processors.academic_processor import AcademicProcessor


# ============================================================
# Setup
# ============================================================

def setup_placement():

    loader = DocumentLoader("data")
    documents = loader.load_documents()

    processor = PlacementProcessor()

    placement_documents = processor.process(
        documents
    )

    embedding_model = EmbeddingModel()

    chroma_store = ChromaVectorStore(
        embedding_model=embedding_model,
        persist_directory="data/chroma_db",
        collection_name="placement_statistics"
    )

    vector_store = chroma_store.get_vector_store()

    bm25 = BM25Retriever(
        placement_documents,
        k=20
    )

    hybrid = HybridRetriever(
        vector_store=vector_store,
        bm25_retriever=bm25,
        k=5,
        fetch_k=20
    )

    return hybrid


def setup_academic():

    loader = DocumentLoader("data")
    documents = loader.load_documents()

    processor = AcademicProcessor()

    academic_documents = processor.process(
        documents
    )

    embedding_model = EmbeddingModel()

    chroma_store = ChromaVectorStore(
        embedding_model=embedding_model,
        persist_directory="data/chroma_db_academic",
        collection_name="academic_courses"
    )

    vector_store = chroma_store.get_vector_store()

    bm25 = BM25Retriever(
        academic_documents,
        k=20
    )

    hybrid = HybridRetriever(
        vector_store=vector_store,
        bm25_retriever=bm25,
        k=5,
        fetch_k=20
    )

    return hybrid


# ============================================================
# RAG
# ============================================================

def run_rag(hybrid_retriever, question):

    # Retrieve
    documents = hybrid_retriever.retrieve(
        question
    )

    # Format context
    formatter = ContextFormatter()

    context = formatter.format_documents(
        documents
    )

    # RAG Prompt
    rag_prompt = RAGPrompt()

    prompt = rag_prompt.get_prompt()

    messages = prompt.format_messages(
        context=context,
        question=question
    )

    # Local LLM
    local_llm = LocalLLM()

    model = local_llm.get_model()

    # Generate answer
    response = model.invoke(
        messages
    )

    return documents, response.content


# ============================================================
# Main
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("RAG EVALUATION")
    print("=" * 70)


    # --------------------------------------------------------
    # Setup retrievers
    # --------------------------------------------------------

    print("\nInitializing Placement Retriever...")
    placement_retriever = setup_placement()

    print("\nInitializing Academic Retriever...")
    academic_retriever = setup_academic()


    # --------------------------------------------------------
    # Questions
    # --------------------------------------------------------

    placement_questions = [

        "What was the placement percentage of IT in 2022-2023?",

        "What was the average salary for IT students in 2022-2023?",

        "What was the highest package for IT in 2023-2024?"

    ]


    academic_questions = [

        "What is the course code for Computer Networks?",

        "What topics are covered in Unit III of Computer Networks?",

        "What addressing versions are covered in the Network Layer unit of Computer Networks?"

    ]


    # ========================================================
    # Placement Tests
    # ========================================================

    print("\n\n")
    print("=" * 70)
    print("PLACEMENT TESTS")
    print("=" * 70)


    for index, question in enumerate(
        placement_questions,
        start=1
    ):

        print("\n" + "-" * 70)
        print(f"PLACEMENT TEST {index}")
        print("-" * 70)

        print("Question:")
        print(question)

        documents, answer = run_rag(
            placement_retriever,
            question
        )

        print("\nTop Retrieved Document:")

        if documents:

            metadata = documents[0].metadata

            print(
                f"Year: {metadata.get('academic_year', 'N/A')}"
            )

            print(
                f"Branch: {metadata.get('branch', 'N/A')}"
            )

        print("\nFinal Answer:")
        print(answer)


    # ========================================================
    # Academic Tests
    # ========================================================

    print("\n\n")
    print("=" * 70)
    print("ACADEMIC TESTS")
    print("=" * 70)


    for index, question in enumerate(
        academic_questions,
        start=1
    ):

        print("\n" + "-" * 70)
        print(f"ACADEMIC TEST {index}")
        print("-" * 70)

        print("Question:")
        print(question)

        documents, answer = run_rag(
            academic_retriever,
            question
        )

        print("\nTop Retrieved Document:")

        if documents:

            metadata = documents[0].metadata

            print(
                f"Course Code: "
                f"{metadata.get('course_code', 'N/A')}"
            )

            print(
                f"Course Name: "
                f"{metadata.get('course_name', 'N/A')}"
            )

            print(
                f"Unit: "
                f"{metadata.get('unit', 'N/A')}"
            )

            print(
                f"Unit Title: "
                f"{metadata.get('unit_title', 'N/A')}"
            )

        print("\nFinal Answer:")
        print(answer)


if __name__ == "__main__":
    main()