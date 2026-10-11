from pipeline.retriever.hybridretriever import HybridRetriever
from pipeline.processors.contextformatter import ContextFormatter
from pipeline.prompts.prompt import RAGPrompt
from pipeline.llm.local_llm import LocalLLM


class RAGPipeline:

    def __init__(self, hybrid_retriever):

        self.hybrid_retriever = hybrid_retriever

        self.context_formatter = ContextFormatter()

        self.rag_prompt = RAGPrompt()

        self.local_llm = LocalLLM()
        self.model = self.local_llm.get_model()

        print("RAG Pipeline initialized")

    def ask(self, question):

        # 1. Retrieve relevant documents
        documents = self.hybrid_retriever.retrieve(question)

        # 2. Convert documents into context
        context = self.context_formatter.format_documents(documents)

        # 3. Create RAG prompt
        prompt = self.rag_prompt.get_prompt()

        # 4. Insert context and question into prompt
        messages = prompt.format_messages(
            context=context,
            question=question
        )

        # 5. Generate answer using local LLM
        response = self.model.invoke(messages)

        return response.content