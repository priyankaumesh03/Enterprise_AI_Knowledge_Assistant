from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from src.retrieval.vector_store import VECTOR_DB_PATH


# Load environment variables
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def generate_answer(question, vector_store=None):

    # 1. Load resources if no cached vector store is provided
    if vector_store is None:

        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vector_store = Chroma(
            collection_name="enterprise_knowledge",
            persist_directory=str(VECTOR_DB_PATH),
            embedding_function=embedding_model
        )

    # 2. Retrieve documents with distance scores
    results = vector_store.similarity_search_with_score(
        question,
        k=3
    )
    # 3. Filter relevant documents
    relevant_documents = [
        document
        for document, score in results
        if score <= 1.3
    ]

    # 4. Reject unknown questions
    if not relevant_documents:
        return (
            "I don't have enough information in my knowledge base "
            "to answer this question.",
            []
        )

    # 5. Prepare context
    context = "\n\n".join(
        document.page_content
        for document in relevant_documents
    )

    # 6. Initialize Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0.2,
        timeout=60,
        max_retries=1
        )
    # 7. Create prompt
    prompt = f"""
    You are an Enterprise Knowledge Assistant.

    Answer the user's question using ONLY the information
    provided in the context below.

    If the answer is not available in the context,
    clearly say that you do not have enough information.

    Context:
    {context}

    User Question:
    {question}

    Answer:
    """

    # 8. Generate answer
    response = llm.invoke(prompt)

    # 9. Extract answer text
    if isinstance(response.content, list):
        answer = "\n".join(
            item["text"]
            for item in response.content
            if item.get("type") == "text"
        )
    else:
        answer = response.content

    # 10. Collect source documents
    sources = sorted({
        Path(document.metadata["source"]).name
        for document in relevant_documents
    })

    return answer, sources


# Terminal testing
if __name__ == "__main__":

    question = input("\nAsk your Enterprise Knowledge Assistant: ")

    answer, sources = generate_answer(question)

    print("\nGENERATED ANSWER:")
    print(answer)

    print("\nSOURCES:")
    for source in sources:
        print("-", source)