from langchain_ollama import ChatOllama


class LocalLLM:

    def __init__(
        self,
        model_name: str = "qwen3:8b"
    ):

        self.model = ChatOllama(
            model=model_name,
            temperature=0
        )

        print(f"Local LLM initialized: {model_name}")

    def get_model(self):

        return self.model