from pipeline.loaders.document_loader import DocumentLoader
from pipeline.splitter.text_splitter import DocumentSplitter


def main():

    # Load documents
    loader = DocumentLoader("data")
    documents = loader.load_documents()

    print(f"Pages loaded: {len(documents)}")

    # Split documents
    splitter = DocumentSplitter()
    chunks = splitter.split_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    # Inspect first chunk
    for i, chunk in enumerate(chunks):

        source = chunk.metadata.get("source", "")

        if "Placement" in source:

            print("\n" + "=" * 70)
            print(f"PLACEMENT CHUNK {i}")
            print("=" * 70)

            print("Page:", chunk.metadata.get("page"))

            print(chunk.page_content)


if __name__ == "__main__":
    main()