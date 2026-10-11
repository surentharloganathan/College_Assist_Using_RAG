class HybridRetriever:

    def __init__(
        self,
        vector_store,
        bm25_retriever,
        k: int = 5,
        fetch_k: int = 20,
        rrf_constant: int = 60
    ):

        self.vector_store = vector_store
        self.bm25_retriever = bm25_retriever

        self.k = k
        self.fetch_k = fetch_k
        self.rrf_constant = rrf_constant


    # ============================================================
    # RETRIEVE
    # ============================================================

    def retrieve(self, query: str):

        print("\n>>> HybridRetriever.retrieve() called")


        # ========================================================
        # 1. Chroma Retrieval
        # ========================================================

        print(">>> Chroma retrieval...")

        chroma_results = self.vector_store.similarity_search(
            query,
            k=self.fetch_k
        )

        print(
            f">>> Chroma returned {len(chroma_results)} documents"
        )


        # ========================================================
        # 2. BM25 Retrieval
        # ========================================================

        print(">>> BM25 retrieval...")

        bm25_results = self.bm25_retriever.retrieve(
            query
        )

        print(
            f">>> BM25 returned {len(bm25_results)} documents"
        )


        # ========================================================
        # 3. RRF Storage
        # ========================================================

        rrf_scores = {}

        documents = {}

        chroma_ranks = {}

        bm25_ranks = {}


        # ========================================================
        # 4. Process Chroma Results
        # ========================================================

        for rank, document in enumerate(
            chroma_results,
            start=1
        ):

            doc_id = self.get_document_id(
                document
            )

            documents[doc_id] = document

            chroma_ranks[doc_id] = rank

            rrf_score = (
                1 / (self.rrf_constant + rank)
            )

            rrf_scores[doc_id] = (
                rrf_scores.get(doc_id, 0)
                + rrf_score
            )


        # ========================================================
        # 5. Process BM25 Results
        # ========================================================

        for rank, item in enumerate(
            bm25_results,
            start=1
        ):

            document, bm25_score = item

            doc_id = self.get_document_id(
                document
            )

            documents[doc_id] = document

            bm25_ranks[doc_id] = rank

            rrf_score = (
                1 / (self.rrf_constant + rank)
            )

            rrf_scores[doc_id] = (
                rrf_scores.get(doc_id, 0)
                + rrf_score
            )


        # ========================================================
        # 6. Metadata-Aware Reranking
        # ========================================================

        final_scores = {}

        for doc_id, document in documents.items():

            rrf_score = rrf_scores[doc_id]

            metadata_score = self.metadata_boost(
                query,
                document
            )

            final_scores[doc_id] = (
                rrf_score + metadata_score
            )


        # ========================================================
        # 7. Final Ranking
        # ========================================================

        ranked_documents = sorted(
            documents.items(),
            key=lambda item: final_scores[item[0]],
            reverse=True
        )



        # ============================================================
        # 8. DEBUG
        # ============================================================

        print("\n" + "=" * 70)
        print("HYBRID RRF + METADATA DEBUG")
        print("=" * 70)

        for i, (doc_id, document) in enumerate(
            ranked_documents[:10],
            start=1
        ):

            print(f"\nRank {i}")

            print(
                "RRF Score:",
                rrf_scores[doc_id]
            )

            print(
                "Metadata Boost:",
                self.metadata_boost(
                    query,
                    document
                )
            )

            print(
                "Final Score:",
                final_scores[doc_id]
            )

            print(
                "Chroma Rank:",
                chroma_ranks.get(
                    doc_id,
                    "Not found"
                )
            )

            print(
                "BM25 Rank:",
                bm25_ranks.get(
                    doc_id,
                    "Not found"
                )
            )

            # --------------------------------------------------------
            # Metadata
            # --------------------------------------------------------

            metadata = document.metadata

            document_type = metadata.get(
                "document_type",
                ""
            )

            print(
                "Document Type:",
                document_type
            )

            # --------------------------------------------------------
            # Academic Document
            # --------------------------------------------------------

            if document_type == "academic_course_unit":

                print(
                    "Course Code:",
                    metadata.get(
                        "course_code",
                        "N/A"
                    )
                )

                print(
                    "Course Name:",
                    metadata.get(
                        "course_name",
                        "N/A"
                    )
                )

                print(
                    "Unit:",
                    metadata.get(
                        "unit",
                        "N/A"
                    )
                )

                print(
                    "Unit Title:",
                    metadata.get(
                        "unit_title",
                        "N/A"
                    )
                )

            # --------------------------------------------------------
            # Placement Document
            # --------------------------------------------------------

            elif document_type == "placement":

                print(
                    "Academic Year:",
                    metadata.get(
                        "academic_year",
                        "N/A"
                    )
                )

                print(
                    "Branch:",
                    metadata.get(
                        "branch",
                        "N/A"
                    )
                )

            # --------------------------------------------------------
            # Common Metadata
            # --------------------------------------------------------

            print(
                "Source:",
                metadata.get(
                    "source",
                    "N/A"
                )
            )

            print(
                "Page:",
                metadata.get(
                    "page",
                    "N/A"
                )
            )
            return [
                document
                for doc_id, document in ranked_documents[:self.k]
            ]
    def get_document_id(self, document):
        metadata = document.metadata

        document_type = metadata.get(
            "document_type",
            ""
        )

        if document_type == "academic_course_unit":
            course_code = metadata.get("course_code", "")
            unit = metadata.get("unit", "")

            return f"{course_code}|{unit}"

        source = metadata.get("source", "")
        page = metadata.get("page", "")

        content_hash = hash(document.page_content)

        return f"{source}|{page}|{content_hash}"
    # ============================================================
    # METADATA BOOST
    # ============================================================

    def metadata_boost(
    self,
    query,
    document
    ):

        """
        Calculate a small ranking boost based on
        document metadata.

        Academic documents:
            - course_code
            - course_name
            - unit
            - unit_title

        Placement documents:
            - branch
            - academic_year
        """

        query_lower = query.lower()

        metadata = document.metadata

        document_type = metadata.get(
            "document_type",
            ""
        ).lower()

        boost = 0.0


        # ============================================================
        # ACADEMIC DOCUMENT
        # ============================================================

        if document_type == "academic_course_unit":

            course_code = str(
                metadata.get(
                    "course_code",
                    ""
                )
            ).lower()

            course_name = str(
                metadata.get(
                    "course_name",
                    ""
                )
            ).lower()

            unit = str(
                metadata.get(
                    "unit",
                    ""
                )
            ).lower()

            unit_title = str(
                metadata.get(
                    "unit_title",
                    ""
                )
            ).lower()


            # --------------------------------------------------------
            # Course Code Exact Match
            # --------------------------------------------------------

            if (
                course_code
                and course_code in query_lower
            ):

                boost += 0.010


            # --------------------------------------------------------
            # Course Name Match
            # --------------------------------------------------------

            if (
                course_name
                and course_name in query_lower
            ):

                boost += 0.008


            # --------------------------------------------------------
            # Unit Match
            # --------------------------------------------------------

            if unit:

                unit_patterns = [

                    f"unit {unit}",

                    f"unit-{unit}",

                    f"unit{unit}"

                ]

                if any(
                    pattern in query_lower
                    for pattern in unit_patterns
                ):

                    boost += 0.010


            # --------------------------------------------------------
            # Unit Title Match
            # --------------------------------------------------------

            if unit_title:

                title_words = unit_title.split()

                matched_words = sum(
                    1
                    for word in title_words
                    if (
                        len(word) > 2
                        and word in query_lower
                    )
                )

                if matched_words > 0:

                    boost += 0.003


        # ============================================================
        # PLACEMENT DOCUMENT
        # ============================================================

        elif document_type == "placement":

            branch = str(
                metadata.get(
                    "branch",
                    ""
                )
            ).lower()

            academic_year = str(
                metadata.get(
                    "academic_year",
                    ""
                )
            ).lower()


            # --------------------------------------------------------
            # Branch Match
            # --------------------------------------------------------

            if (
                branch
                and branch in query_lower
            ):

                boost += 0.010


            # --------------------------------------------------------
            # Academic Year Match
            # --------------------------------------------------------

            if (
                academic_year
                and academic_year in query_lower
            ):

                boost += 0.010


        return boost