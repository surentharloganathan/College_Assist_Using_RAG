from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(
        self,
        documents,
        k=20
    ):

        self.documents = documents
        self.k = k

        # Tokenize documents
        tokenized_documents = [
            document.page_content.lower().split()
            for document in documents
        ]

        # Create BM25 index
        self.bm25 = BM25Okapi(
            tokenized_documents
        )

        print("BM25 Retriever initialized")


    def retrieve(self, query):

        # Tokenize query
        tokenized_query = query.lower().split()

        # Get BM25 scores
        scores = self.bm25.get_scores(
            tokenized_query
        )

        # Rank documents
        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )

        # Return top K with scores
        results = []

        for index in ranked_indices[:self.k]:
            if scores[index] <= 0:
                 continue
            results.append(
                (
                    self.documents[index],
                    scores[index]
                )
            )
            if len(results) >= self.k:
                break


        return results