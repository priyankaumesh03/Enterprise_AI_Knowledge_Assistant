from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.ingestion.load_documents import load_documents


def chunk_documents(documents):

    print("Splitting documents into chunks...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)

    print(f"\nTotal chunks created: {len(chunks)}")

    for i, chunk in enumerate(chunks[:5]):
        print(f"\n--- Chunk {i + 1} ---")
        print(f"Source: {chunk.metadata['source']}")
        print(f"Characters: {len(chunk.page_content)}")
        print(chunk.page_content[:200])

    return chunks


if __name__ == "__main__":

    documents = load_documents()

    chunks = chunk_documents(documents)