from pipeline.llm.local_llm import LocalLLM


def main():

    llm = LocalLLM()

    model = llm.get_model()

    response = model.invoke(
        "What is 2 + 2?"
    )

    print("\n" + "=" * 70)
    print("LOCAL LLM RESPONSE")
    print("=" * 70)

    print(response.content)


if __name__ == "__main__":
    main()