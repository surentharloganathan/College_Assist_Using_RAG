from pipeline.loaders.document_loader import DocumentLoader
from pipeline.processors.academic_processor import AcademicProcessor


# ============================================================
# LOAD DOCUMENTS
# ============================================================

loader = DocumentLoader("data")

documents = loader.load_documents()

print("\nTotal pages:", len(documents))


# ============================================================
# PROCESS ACADEMIC DOCUMENTS
# ============================================================

processor = AcademicProcessor()

academic_documents = processor.process(documents)
# ============================================================
# VALIDATE COURSE DOCUMENT STRUCTURE
# ============================================================

course_stats = {}

for document in academic_documents:

    code = str(
        document.metadata.get("course_code", "")
    ).strip()

    if not code:
        continue

    document_type = document.metadata.get(
        "document_type",
        ""
    )

    unit = document.metadata.get(
        "unit"
    )

    if code not in course_stats:
        course_stats[code] = {
            "name": document.metadata.get("course_name", ""),
            "total": 0,
            "units": []
        }

    course_stats[code]["total"] += 1

    if unit:
        course_stats[code]["units"].append(unit)


print("\n" + "=" * 80)
print("COURSE STRUCTURE VALIDATION")
print("=" * 80)

for code, data in course_stats.items():

    unit_count = len(data["units"])

    print(
        f"{code:12} | "
        f"{data['name'][:45]:45} | "
        f"Documents: {data['total']:2} | "
        f"Units: {unit_count}"
    )

print("=" * 80)
print(
    "Total unique courses:",
    len(course_stats)
)
print(
    "\nAcademic unit documents:",
    len(academic_documents)
)


# ============================================================
# DEBUG - SHOW ALL DETECTED COURSES
# ============================================================

courses = {}

for document in academic_documents:

    course_code = str(
        document.metadata.get(
            "course_code",
            ""
        )
    ).strip()

    course_name = str(
        document.metadata.get(
            "course_name",
            ""
        )
    ).strip()

    if course_code and course_code not in courses:

        courses[course_code] = course_name


print("\n" + "=" * 80)
print("DETECTED COURSES")
print("=" * 80)

for code, name in courses.items():

    print(
        f"{code} -> {name}"
    )

print(
    "\nTotal unique courses:",
    len(courses)
)

print("=" * 80)


# ============================================================
# USER QUERY
# ============================================================

query = input(
    "\nEnter course code or exact course name: "
).strip().lower()


# ============================================================
# SEARCH
# ============================================================

print("\n" + "=" * 80)
print("SEARCH RESULTS")
print("=" * 80)


matched_documents = []

for document in academic_documents:

    course_code = str(
        document.metadata.get(
            "course_code",
            ""
        )
    ).strip().lower()

    course_name = str(
        document.metadata.get(
            "course_name",
            ""
        )
    ).strip().lower()

    # Exact course code OR exact course name
    if query == course_code or query == course_name:

        matched_documents.append(document)


# ============================================================
# DISPLAY RESULT
# ============================================================

if not matched_documents:

    print("\nNo exact matching course found.")

else:

    # --------------------------------------------------------
    # Course information
    # --------------------------------------------------------

    first_document = matched_documents[0]

    print("\n" + "-" * 80)

    print(
        "Course Code:",
        first_document.metadata.get(
            "course_code"
        )
    )

    print(
        "Course Name:",
        first_document.metadata.get(
            "course_name"
        )
    )

    print(
        "Semester:",
        first_document.metadata.get(
            "semester"
        )
    )

    print(
        "Credits:",
        first_document.metadata.get(
            "credits",
            "Unknown"
        )
    )

    print(
        "Document Type:",
        first_document.metadata.get(
            "document_type"
        )
    )

    # --------------------------------------------------------
    # Units
    # --------------------------------------------------------

    print("\nUnits:")

    units = []

    for document in matched_documents:

        unit = document.metadata.get(
            "unit"
        )

        unit_title = document.metadata.get(
            "unit_title"
        )

        if unit:

            units.append(
                (
                    unit,
                    unit_title
                )
            )

    # Sort units
    units.sort(
        key=lambda x: [
            "I",
            "II",
            "III",
            "IV",
            "V"
        ].index(x[0])
        if x[0] in [
            "I",
            "II",
            "III",
            "IV",
            "V"
        ]
        else 99
    )

    if units:

        for unit, title in units:

            print(
                f"  Unit {unit}: {title}"
            )

    else:

        print(
            "  No unit documents found."
        )

    print("\n" + "-" * 80)

    print(
        "Matched documents:",
        len(matched_documents)
    )