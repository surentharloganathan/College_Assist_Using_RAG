from pipeline.prompts.prompt import RAGPrompt
from pipeline.llm.local_llm import LocalLLM

def main():

    # --------------------------------
    # Context
    # --------------------------------

    context = """
[Document 1]
Document Type: placement
Academic Year: 2022-2023
Branch: CIVIL

Intake: 131
Eligible Students: 107
Students Placed: 67
Placement Percentage: 62.61%

Minimum Salary: 2.1 LPA
Average Salary: 7.8 LPA
Maximum Salary: 13.5 LPA

Company: SOBHA
"""

    # --------------------------------
    # User Question
    # --------------------------------

    question = (
        "What is the placement percentage of the IT in 2023-2024"
    )

    # --------------------------------
    # Create RAG Prompt
    # --------------------------------

    rag_prompt = RAGPrompt()

    prompt = rag_prompt.get_prompt()

    
     # Initializing the local LLm 
    local_llm = LocalLLM()

    model = local_llm.get_model()


    # --------------------------------
    # Create messages
    # --------------------------------

    messages = prompt.format_messages(
        context=context,
        question=question
    )

    # --------------------------------
    # Send to Local llm
    # --------------------------------

    response = model.invoke(messages)

# --------------------------------
    # Display answer
    # --------------------------------

    print("\n" + "=" * 70)
    print("Local LLM RAG RESPONSE")
    print("=" * 70)

    print(response.content)


if __name__ == "__main__":
    main()