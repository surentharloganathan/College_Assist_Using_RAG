from pipeline.rag.rag_pipeline import RAGPipeline


class RAGRouter:

    def __init__(self, academic_retriever, placement_retriever):

        self.academic_pipeline = RAGPipeline(
            academic_retriever
        )

        self.placement_pipeline = RAGPipeline(
            placement_retriever
        )

        print("RAG Router initialized")

    def route(self, question):

        question_lower = question.lower()

        placement_keywords = [
            "placement",
            "placed",
            "salary",
            "package",
            "highest package",
            "average salary",
            "minimum salary",
            "maximum salary",
            "company"
        ]

        for keyword in placement_keywords:
            if keyword in question_lower:
                print("Router: Placement")
                return self.placement_pipeline.ask(question)

        print("Router: Academic")
        return self.academic_pipeline.ask(question)