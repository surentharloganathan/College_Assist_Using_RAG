from pipeline.loaders.document_loader import DocumentLoader
from pipeline.processors.placement_processors import PlacementProcessor
from pipeline.processors.academic_processor import AcademicProcessor
from pipeline.processors.contextformatter import ContextFormatter


def main():

    # -------------------------------
    # Load documents
    # -------------------------------
    
    data_path = "data"
    loader = DocumentLoader(data_path)

    documents = loader.load_documents()

    print("\nTotal documents loaded:", len(documents))


    # -------------------------------
    # Process placement documents
    # -------------------------------

    placement_processor = PlacementProcessor()

    placement_documents = placement_processor.process(
        documents
    )

    print(
        "Placement documents:",
        len(placement_documents)
    )


    # -------------------------------
    # Context Formatter
    # -------------------------------

    formatter = ContextFormatter()

    context = formatter.format_documents(
        placement_documents[:3]
    )


    # -------------------------------
    # Display formatted context
    # -------------------------------

    print("\n")
    print("=" * 70)
    print("FORMATTED CONTEXT")
    print("=" * 70)

    print(context)


if __name__ == "__main__":
    main()