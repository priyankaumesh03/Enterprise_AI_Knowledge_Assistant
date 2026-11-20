from sentence_transformers import SentenceTransformer
from src.chunking.chunk_documents import chunk_documents
from src.ingestion.load_documents import load_documents


def generate_embeddings(chunks):

    print("\nLoading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Generating embeddings...")

    texts = [chunk.page_content for chunk in chunks]

    embeddings = model.encode(texts)

    print("\nEmbedding generation successful!")

    print("Number of chunks:", len(embeddings))
    print("Embedding dimensions:", embeddings.shape)

    return embeddings, model


if __name__ == "__main__":

    documents = load_documents()

    chunks = chunk_documents(documents)

    embeddings, model = generate_embeddings(chunks)

    print("\nFirst embedding preview:")
    print(embeddings[0][:10])