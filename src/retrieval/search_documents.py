from pathlib import Path
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from src.retrieval.vector_store import VECTOR_DB_PATH


def search_documents(query, k=3):

    print(f"\nSearching for: {query}")

    # Load the embedding model
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Load the existing ChromaDB database
    vector_store = Chroma(
        collection_name="enterprise_knowledge",
        persist_directory=str(VECTOR_DB_PATH),
        embedding_function=embedding_model
    )

    # Perform semantic similarity search
    results = vector_store.similarity_search_with_score(
        query,
        k=k
    )

    print(f"\nTop {k} relevant chunks found:")

    for i, (document, score) in enumerate(results, start=1):

        print(f"\n{'=' * 50}")
        print(f"Result {i}")
        print(f"Distance score: {score:.4f}")
        print(f"Source: {Path(document.metadata['source']).name}")
        print("\nContent:")
        print(document.page_content)


if __name__ == "__main__":

    question = "What should employees do when manufacturing equipment suddenly stops working?"
    search_documents(question, k=3)