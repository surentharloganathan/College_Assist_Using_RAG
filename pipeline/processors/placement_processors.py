from langchain_core.documents import Document


class PlacementProcessor:

    def process(self, documents):

        structured_documents = []

        for document in documents:

            source = document.metadata.get(
                "source",
                ""
            )

            # Process only placement PDFs
            if "Placement_" not in source:
                continue

            structured = self._process_placement_document(
                document
            )

            structured_documents.extend(
                structured
            )

        return structured_documents


    def _process_placement_document(
        self,
        document
    ):

        text = document.page_content

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        structured_documents = []


        # Determine academic year
        if "2022-2023" in text or "2022-2023" in document.metadata.get("source", ""):
            academic_year = "2022-2023"

        elif "2023-2024" in text or "2023-2024" in document.metadata.get("source", ""):
            academic_year = "2023-2024"

        else:
            academic_year = "Unknown"


        for line in lines:

            parts = line.split()

            if not parts:
                continue

            if not parts[0].isdigit():
                continue

            if len(parts) < 10:
                continue

            try:

                serial_no = parts[0]
                branch = parts[1]

                intake = parts[2]
                eligible = parts[3]
                placed = parts[4]
                percentage = parts[5]

                salary_min = parts[6]
                salary_average = parts[7]
                salary_max = parts[8]

                company = " ".join(parts[9:])

            except IndexError:

                continue


            structured_text = f"""
Academic Year: {academic_year}
Document Type: Placement Statistics

Branch: {branch}
Intake: {intake}
Eligible Students: {eligible}
Students Placed: {placed}
Placement Percentage: {percentage}%

Minimum Salary: {salary_min} LPA
Average Salary: {salary_average} LPA
Maximum Salary: {salary_max} LPA

Company: {company}
""".strip()


            structured_documents.append(
                Document(
                    page_content=structured_text,

                    metadata={
                        **document.metadata,
                        "document_type": "placement",
                        "branch": branch,
                        "academic_year": academic_year
                    }
                )
            )

        return structured_documents