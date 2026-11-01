from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class DocumentLoader:

    def __init__(self, data_path: str):
        self.data_path = Path(data_path)

    def load_documents(self) -> list[Document]:

        documents = []

        pdf_files = list(self.data_path.glob("*.pdf"))

        print(f"Found {len(pdf_files)} PDF files")

        for pdf_file in pdf_files:

            print(f"\nLoading: {pdf_file.name}")

            loader = PyPDFLoader(str(pdf_file))

            docs = loader.load()

            print(f"Pages loaded: {len(docs)}")

            documents.extend(docs)

        print("\n-----------------------------")
        print(f"Total pages loaded: {len(documents)}")
        print("-----------------------------")

        return documents