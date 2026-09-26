from langchain_core.prompts import ChatPromptTemplate


class RAGPrompt:

    def __init__(self):

        self.prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI assistant for the Information Technology
department of Government College of Technology, Coimbatore.

You must answer the user's question ONLY using the information
provided in the Context.

STRICT RULES:

1. Do not use your general knowledge.
2. Do not make assumptions.
3. Do not guess or estimate.
4. Do not provide information that is not present in the Context.
5. If the Context does not contain enough information to answer
   the question, respond exactly:

   "I couldn't find enough information in the provided
   college documents to answer this question."

6. When the Context contains the answer, give the answer
   directly and clearly.

Context:
{context}
"""
        ),
        (
            "human",
            "{question}"
        )
    ]
)

    def get_prompt(self):

        return self.prompt