import re
from langchain_core.documents import Document


class AcademicProcessor:

    def process(self, documents):

        structured_documents = []

        current_course = None

        for document in documents:

            source = document.metadata.get("source", "")

            # Only process the 2022 IT curriculum
            if "REG22_IT_All" not in source:
                continue

            text = document.page_content.strip()

            if not text:
                continue

            # ---------------------------------------------------------
            # Detect course heading
            #
            # Course headings can appear at the END of one PDF page
            # while PREREQUISITES appears on the NEXT page.
            #
            # Therefore we detect the course heading independently
            # of PREREQUISITES.
            # ---------------------------------------------------------
            text = document.page_content

            normalized_text = re.sub(r"[ \t]+", " ", text)
            normalized_text = re.sub(r" *\n *", "\n", normalized_text)
            course_match = re.search(
                r"(?m)^\s*"
                r"(22[A-Z0-9#$]{4,8})"
                r"\s+"

                # Optional regional-language text between code and English name
                r"(?:[^\x00-\x7F][^\r\n]*\r?\n\s*)?"

                r"([A-Z][A-Za-z0-9&$#.,'()/\- ]{2,100}?)"
                r"\s*"

                r"(?:\r?\n\s*)?"

                r"(?:"
                    r"\(Common\s+to\s+[^)]*\)"
                    r"\s*"
                r")?"

                r"(?:"
                    r"\s*SEMESTER\s*"
                    r"(VIII|VII|VI|V|IV|III|II|I)"
                r")?"

                r"\s*$",

                normalized_text,
                re.IGNORECASE
            )

            if course_match:

                # -----------------------------------------------------
                # Save previous course
                # -----------------------------------------------------

                if current_course:

                    structured_documents.extend(
                        self._create_course_documents(
                            current_course
                        )
                    )

                # -----------------------------------------------------
                # Extract course information
                # -----------------------------------------------------

                course_code = course_match.group(1).strip()

                course_name = course_match.group(2).strip()

                # Clean course name
                course_name = re.sub(
                    r"\s+",
                    " ",
                    course_name
                ).strip()

                # -----------------------------------------------------
                # Semester
                # -----------------------------------------------------
                semester_match = re.search(
                    r"SEMESTER\s*(VIII|VII|VI|V|IV|III|II|I)\b",
                    normalized_text,
                    re.IGNORECASE
                )

                semester = (
                    semester_match.group(1).upper()
                    if semester_match
                    else "Unknown"
                )
                # -----------------------------------------------------
                # Create current course
                # -----------------------------------------------------

                current_course = {

                    "course_code": course_code,

                    "course_name": course_name,

                    "semester": semester,

                    "content": text,

                    "metadata": document.metadata
                }

            else:

                # -----------------------------------------------------
                # Continue previous course across pages
                # -----------------------------------------------------

                if current_course:

                    current_course["content"] += (
                        "\n" + text
                    )

            # -------------------------------------------------------------
            # Save final course
            # -------------------------------------------------------------

            if current_course:

                structured_documents.extend(
                    self._create_course_documents(
                        current_course
                    )
                )


                # -------------------------------------------------------------
                # Remove duplicate course-unit documents
                # -------------------------------------------------------------

            unique_documents = {}

            for document in structured_documents:

                course_code = document.metadata.get(
                    "course_code",
                    ""
                )

                unit = document.metadata.get(
                    "unit",
                    ""
                )

                document_type = document.metadata.get(
                    "document_type",
                    ""
                )

                key = (
                    course_code,
                    unit,
                    document_type
                )

                if key not in unique_documents:

                    unique_documents[key] = document


        structured_documents = list(
            unique_documents.values()
        )


        return structured_documents

    # ================================================================
    # CREATE COURSE DOCUMENTS
    # ================================================================

    def _create_course_documents(self, course):

        content = course["content"]

        course_code = course["course_code"]

        course_name = course["course_name"]

        semester = course["semester"]

        # -------------------------------------------------------------
        # Extract course details
        # -------------------------------------------------------------

        prerequisites = "Unknown"
        category = "Unknown"
        lecture = "Unknown"
        tutorial = "Unknown"
        practical = "Unknown"
        credits = "Unknown"

        # -------------------------------------------------------------
        # LTPC
        #
        # Example:
        #
        # PREREQUISITES CATEGORY L T P C
        # NIL PC 3 0 0 3
        # -------------------------------------------------------------

        ltpc_match = re.search(
            r"PREREQUISITES\s+"
            r"CATEGORY\s+"
            r"L\s+T\s+P\s+C\s+"
            r"([A-Za-z0-9$\/\-]+)\s+"
            r"([A-Za-z0-9$\/\-]+)\s+"
            r"(\d+(?:\.\d+)?)\s+"
            r"(\d+(?:\.\d+)?)\s+"
            r"(\d+(?:\.\d+)?)\s+"
            r"(\d+(?:\.\d+)?)",
            content,
            re.IGNORECASE
        )

        if ltpc_match:

            prerequisites = ltpc_match.group(1)

            category = ltpc_match.group(2)

            lecture = ltpc_match.group(3)

            tutorial = ltpc_match.group(4)

            practical = ltpc_match.group(5)

            credits = ltpc_match.group(6)

        # -------------------------------------------------------------
        # Find UNIT sections
        # -------------------------------------------------------------

        unit_pattern = re.compile(
            r"""
            UNIT
            \s*
            [–—-]
            \s*
            (?P<unit>[IVX]+)
            \s+
            (?P<content>.*?)
            (?=
                UNIT\s*[–—-]\s*[IVX]+\s+
                |
                CONTACT\s+PERIODS
                |
                TEXT\s+BOOK
                |
                TEXT\s+BOOKS
                |
                REFERENCES
                |
                COURSE\s+OUTCOMES
                |
                COURSE\s+ARTICULATION
                |
                $
            )
            """,
            re.IGNORECASE |
            re.DOTALL |
            re.VERBOSE
        )

        unit_matches = list(
            unit_pattern.finditer(content)
        )
        # Remove duplicate UNIT sections
        unique_units = {}

        for match in unit_matches:

            unit_number = match.group("unit").upper().strip()

            if unit_number not in unique_units:
                unique_units[unit_number] = match


        unit_matches = list(unique_units.values())

        documents = []

        # =============================================================
        # UNIT DOCUMENTS
        # =============================================================

        if unit_matches:

            for match in unit_matches:

                unit_number = (
                    match.group("unit")
                    .upper()
                    .strip()
                )

                unit_content = (
                    match.group("content")
                    .strip()
                )

                # -----------------------------------------------------
                # Extract unit title
                #
                # Example:
                #
                # BASICS OF POWER SYSTEMS 9 Periods
                #
                # -----------------------------------------------------

                title_match = re.match(
                    r"(?P<title>.*?)(?:\s+\d+\s+Periods?)"
                    r"(?:\s+|$)",
                    unit_content,
                    re.IGNORECASE |
                    re.DOTALL
                )

                if title_match:

                    unit_title = (
                        title_match.group("title")
                        .strip()
                    )

                    unit_body = (
                        unit_content[
                            title_match.end():
                        ].strip()
                    )

                else:

                    # Fallback
                    lines = unit_content.split(
                        "\n",
                        1
                    )

                    unit_title = (
                        lines[0].strip()
                    )

                    unit_body = (
                        lines[1].strip()
                        if len(lines) > 1
                        else unit_content
                    )

                # -----------------------------------------------------
                # Structured content
                # -----------------------------------------------------

                structured_text = f"""
Document Type: Academic Course Unit

Programme: B.Tech Information Technology

Regulation: 2022

Course Code: {course_code}

Course Name: {course_name}

Semester: {semester}

Unit: {unit_number}

Unit Title: {unit_title}

Prerequisites: {prerequisites}

Category: {category}

Lecture: {lecture}

Tutorial: {tutorial}

Practical: {practical}

Credits: {credits}

Unit Content:

{unit_body}
""".strip()

                # -----------------------------------------------------
                # LangChain Document
                # -----------------------------------------------------

                documents.append(
                    Document(
                        page_content=structured_text,

                        metadata={
                            **course["metadata"],

                            "document_type":
                                "academic_course_unit",

                            "course_code":
                                course_code,

                            "course_name":
                                course_name,

                           "credits": credits,

                            "semester":
                                semester,

                            "unit":
                                unit_number,

                            "unit_title":
                                unit_title,

                            "regulation":
                                "2022"
                        }
                    )
                )

        # =============================================================
        # COURSE WITHOUT UNIT SECTIONS
        # =============================================================

        else:

            structured_text = f"""
Document Type: Academic Course

Programme: B.Tech Information Technology

Regulation: 2022

Course Code: {course_code}

Course Name: {course_name}

Semester: {semester}

Prerequisites: {prerequisites}

Category: {category}

Lecture: {lecture}

Tutorial: {tutorial}

Practical: {practical}

Credits: {credits}

Course Content:

{content}
""".strip()

            documents.append(
                Document(
                    page_content=structured_text,

                  metadata = {
                    **course["metadata"],
                    "course_code": course_code,
                    "course_name": course_name,
                    "credits": credits,
                    "semester": semester,
                    "regulation": "2022",
}
                )
            )

        return documents