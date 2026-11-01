class ContextFormatter:

    def __init__(self):
        print("Context Formatter initialized")

    def format_documents(self, documents):
        """
        Convert retrieved LangChain Documents
        into clean context for the LLM.
        """

        if not documents:
            return ""

        formatted_documents = []

        for index, document in enumerate(documents, start=1):

            metadata = document.metadata
            content = document.page_content.strip()

            document_type = metadata.get(
                "document_type",
                "unknown"
            )

            # --------------------------------
            # Placement Document
            # --------------------------------
            if document_type == "placement":

                formatted_text = f"""[Document {index}]
Document Type: placement
Academic Year: {metadata.get("academic_year", "N/A")}
Branch: {metadata.get("branch", "N/A")}

{self.remove_redundant_placement_metadata(content)}
"""

            # --------------------------------
            # Academic Document
            # --------------------------------
            elif document_type == "academic_course_unit":

                formatted_text = f"""[Document {index}]
Document Type: academic_course_unit
Course Code: {metadata.get("course_code", "N/A")}
Course Name: {metadata.get("course_name", "N/A")}
Semester: {metadata.get("semester", "N/A")}
Unit: {metadata.get("unit", "N/A")}
Unit Title: {metadata.get("unit_title", "N/A")}

Content:
{content}
"""

            # --------------------------------
            # General Document
            # --------------------------------
            else:

                formatted_text = f"""[Document {index}]
Document Type: {document_type}

Content:
{content}
"""

            formatted_documents.append(
                formatted_text.strip()
            )

        return "\n\n".join(formatted_documents)

    def remove_redundant_placement_metadata(self, content):
        """
        Remove placement fields that are already
        represented using document metadata.
        """

        lines = content.splitlines()

        cleaned_lines = []

        fields_to_remove = {
            "Academic Year:",
            "Document Type:",
            "Branch:"
        }

        for line in lines:

            stripped_line = line.strip()

            if any(
                stripped_line.startswith(field)
                for field in fields_to_remove
            ):
                continue

            cleaned_lines.append(line)

        return "\n".join(cleaned_lines).strip()