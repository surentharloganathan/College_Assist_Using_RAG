from pipeline.loaders.document_loader import DocumentLoader
from pipeline.processors.academic_processor import AcademicProcessor
from pipeline.embeddings.embedding_model import EmbeddingModel
from pipeline.vectorstore.chroma_store import ChromaVectorStore
from pipeline.retriever.hybridretriever import HybridRetriever
from pipeline.retriever.bm25_retriever import BM25Retriever

def main():

    # 1. Load documents
    loader = DocumentLoader("data")
    documents = loader.load_documents()

    # 2. Process academic documents
    processor = AcademicProcessor()
    academic_documents = processor.process(documents)

    print("\nAcademic documents:", len(academic_documents))

    # 3. Create embedding model
    embedding_model = EmbeddingModel()

    # 4. Create Chroma vector store
    vector_store = ChromaVectorStore(
        embedding_model,
        persist_directory="data/chroma_db_academic"
    )

    # 5. Store academic documents
    vector_store.add_documents(academic_documents)

    # 6. Create hybrid retriever
    bm25_retriever = BM25Retriever(academic_documents)

    retriever = HybridRetriever(
        vector_store=vector_store,
        bm25_retriever=bm25_retriever
    )

    # 7. Take user question
    query = input("\nEnter your question: ")

    # 8. Retrieve relevant documents
    results = retriever.retrieve(query)

    # 9. Display results
    print("\n" + "=" * 70)
    print("USER QUESTION")
    print("=" * 70)
    print(query)

    print("\n" + "=" * 70)
    print("RETRIEVED DOCUMENTS")
    print("=" * 70)
    
    for i, document in enumerate(results, start=1):

        print(f"\n--- Result {i} ---")

        print(
            "Course Code:",
            document.metadata.get("course_code", "Unknown")
        )

        print(
            "Course Name:",
            document.metadata.get("course_name", "Unknown")
        )

        print(
            "Semester:",
            document.metadata.get("semester", "Unknown")
        )

        print(
            "Credits:",
            document.page_content.split("Credits:")[1]
            .split("\n")[0].strip()
            if "Credits:" in document.page_content
            else "Unknown"
        )

        print("\nContent:")
        print(document.page_content[:500])


if __name__ == "__main__":
    main()



# a check for the first and  second sem Syllabus

# import re

# from pipeline.loaders.document_loader import DocumentLoader


# def main():
#     loader = DocumentLoader("data")
#     documents = loader.load_documents()

#     print("=" * 70)
#     print("SEMESTER I AND II COURSE HEADINGS")
#     print("=" * 70)

#     for document in documents:
#         source = document.metadata.get("source", "")

#         if "REG22_IT_All" not in source:
#             continue

#         text = document.page_content

#         semester_match = re.search(
#             r"\bSEMESTER\s+(I|II)\b",
#             text,
#             re.IGNORECASE
#         )

#         if semester_match:
#             print("\n" + "-" * 70)
#             print("Page:", document.metadata.get("page"))
#             print("-" * 70)

#             # Print the end as well because course headings
#             # may appear at the bottom of the extracted page.
#             print(text[:3000])


# if __name__ == "__main__":
#     main()



# Temprorary Test For the Computer Network Query

# from pipeline.loaders.document_loader import DocumentLoader


# def main():

#     loader = DocumentLoader("data")
#     documents = loader.load_documents()

#     print("\n" + "=" * 70)
#     print("SEARCHING FOR 22IPC509 COMPUTER NETWORKS")
#     print("=" * 70)

#     for document in documents:

#         source = document.metadata.get("source", "")

#         if "REG22_IT_All" not in source:
#             continue

#         text = document.page_content

#         if "22IPC509" in text.upper():

#             print("\n" + "-" * 70)
#             print("PAGE:", document.metadata.get("page"))
#             print("-" * 70)

#             print(text)


# if __name__ == "__main__":
#     main()




# Code for Checking Elective courses

# from pipeline.loaders.document_loader import DocumentLoader


# loader = DocumentLoader("data")

# documents = loader.load_documents()

# print("\n" + "=" * 80)
# print("RAW TEXT FOR 22EOE$06")
# print("=" * 80)

# for document in documents:

#     source = document.metadata.get("source", "")

#     if "REG22_IT_All" not in source:
#         continue

#     text = document.page_content

#     if "22EOE$06" in text.upper():

#         print("\n" + "-" * 80)
#         print("PAGE:", document.metadata.get("page"))
#         print("-" * 80)

#         print(text)