from pipeline.loaders.document_loader import DocumentLoader
from pipeline.processors.placement_processors import PlacementProcessor


def main():

    # ==========================================
    # 1. Load Documents
    # ==========================================

    loader = DocumentLoader("data")

    documents = loader.load_documents()

    print(
        f"\nPages loaded: {len(documents)}"
    )


    # ==========================================
    # 2. Find Placement 2022-2023
    # ==========================================

    placement_document = None

    for document in documents:

        source = document.metadata.get(
            "source",
            ""
        )

        page = document.metadata.get(
            "page"
        )

        if (
            "Placement_" in source
            and page == 0
        ):

            placement_document = document

            break


    if placement_document is None:

        print(
            "Placement document not found."
        )

        return


    # ==========================================
    # 3. Process Placement Document
    # ==========================================

    processor = PlacementProcessor()

    structured_documents = processor.process(
        [placement_document]
    )


    # ==========================================
    # 4. Display
    # ==========================================

    print("\n" + "=" * 70)
    print("STRUCTURED PLACEMENT DATA")
    print("=" * 70)

    print(
        f"\nRows created: "
        f"{len(structured_documents)}"
    )


    for i, document in enumerate(
        structured_documents,
        start=1
    ):

        print(f"\nRow {i}")
        print("-" * 70)

        print(
            document.page_content
        )

        print(
            "\nMetadata:",
            document.metadata
        )


if __name__ == "__main__":
    main()