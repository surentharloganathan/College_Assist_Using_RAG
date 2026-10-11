from flask import Flask, request, jsonify

from pipeline.vectorstore.chroma_store import ChromaVectorStore
from pipeline.embeddings.embedding_model import EmbeddingModel

from pipeline.retriever.bm25_retriever import BM25Retriever
from pipeline.retriever.hybridretriever import HybridRetriever

from pipeline.loaders.document_loader import DocumentLoader
from pipeline.processors.placement_processors import PlacementProcessor
from pipeline.processors.academic_processor import AcademicProcessor

from pipeline.rag.rag_router import RAGRouter


app = Flask(__name__)


# --------------------------------------------------
# Initialize documents
# --------------------------------------------------

print("Loading documents...")

loader = DocumentLoader("data")
documents = loader.load_documents()


# --------------------------------------------------
# Process Placement Documents
# --------------------------------------------------

placement_processor = PlacementProcessor()
placement_documents = placement_processor.process(documents)


# --------------------------------------------------
# Process Academic Documents
# --------------------------------------------------

academic_processor = AcademicProcessor()
academic_documents = academic_processor.process(documents)


# --------------------------------------------------
# Load Embedding Model
# --------------------------------------------------

embedding_model = EmbeddingModel()


# --------------------------------------------------
# Connect to Placement Chroma
# --------------------------------------------------

placement_chroma = ChromaVectorStore(
    embedding_model=embedding_model,
    persist_directory="data/chroma_db",
    collection_name="placement_statistics"
)

placement_vector_store = placement_chroma.get_vector_store()


# --------------------------------------------------
# Connect to Academic Chroma
# --------------------------------------------------

academic_chroma = ChromaVectorStore(
    embedding_model=embedding_model,
    persist_directory="data/chroma_db_academic",
    collection_name="academic_courses"
)

academic_vector_store = academic_chroma.get_vector_store()


# --------------------------------------------------
# Create Placement BM25
# --------------------------------------------------

placement_bm25 = BM25Retriever(
    placement_documents,
    k=20
)


# --------------------------------------------------
# Create Academic BM25
# --------------------------------------------------

academic_bm25 = BM25Retriever(
    academic_documents,
    k=20
)


# --------------------------------------------------
# Create Placement Hybrid Retriever
# --------------------------------------------------

placement_retriever = HybridRetriever(
    vector_store=placement_vector_store,
    bm25_retriever=placement_bm25,
    k=5,
    fetch_k=20
)


# --------------------------------------------------
# Create Academic Hybrid Retriever
# --------------------------------------------------

academic_retriever = HybridRetriever(
    vector_store=academic_vector_store,
    bm25_retriever=academic_bm25,
    k=5,
    fetch_k=20
)


# --------------------------------------------------
# Create RAG Router
# --------------------------------------------------

router = RAGRouter(
    academic_retriever=academic_retriever,
    placement_retriever=placement_retriever
)


print("RAG API initialized successfully")


# --------------------------------------------------
# API Endpoint
# --------------------------------------------------

@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({
            "error": "Question is required"
        }), 400

    question = data["question"].strip()

    if not question:
        return jsonify({
            "error": "Question cannot be empty"
        }), 400

    try:

        answer = router.route(question)

        return jsonify({
            "question": question,
            "answer": answer
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "RAG API is running"
    })


# --------------------------------------------------
# Start Server
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )   