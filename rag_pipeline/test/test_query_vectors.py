from pipeline.embeddings.embedding_model import EmbeddingModel


def main():

    embedding_model = EmbeddingModel()

    query = "What is the placement percentage of IT?"

    query_vector = embedding_model.embed_query(query)

    print("\nQuery embedding created!")

    print("Query vector dimensions:", len(query_vector))

    print("\nFirst 10 values:")
    print(query_vector[:10])


if __name__ == "__main__":
    main()