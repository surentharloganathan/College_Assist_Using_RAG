from pipeline.loaders.document_loader import DocumentLoader


loader = DocumentLoader("data")
documents = loader.load_documents()

print("\nSearching for 22IPC509...\n")

found = False

for i, document in enumerate(documents):

    text = document.page_content

    if "22IPC509" in text:

        found = True

        print("=" * 100)
        print(f"FOUND ON LOADER PAGE: {i}")
        print("=" * 100)

        index = text.find("22IPC509")

        start = max(0, index - 1000)
        end = min(len(text), index + 4000)

        print(text[start:end])
        print()

if not found:
    print("22IPC509 was NOT found in the extracted PDF text.")