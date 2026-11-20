from pathlib import Path
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from src.ingestion.load_documents import load_documents
from src.chunking.chunk_documents import chunk_documents


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Vector database storage location
VECTOR_DB_PATH = PROJECT_ROOT / "vector_store" / "chroma_db"


def create_vector_store():

    print("Loading documents...")

    documents = load_documents()

    print("\nCreating document chunks...")

    chunks = chunk_documents(documents)

    print("\nLoading embedding model...")

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("\nCreating ChromaDB vector store...")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=str(VECTOR_DB_PATH),
        collection_name="enterprise_knowledge"
    )

    print("\nVector database created successfully!")

    print("Total chunks stored:", vector_store._collection.count())

    print("Database location:", VECTOR_DB_PATH)

    return vector_store


if __name__ == "__main__":

    create_vector_store()