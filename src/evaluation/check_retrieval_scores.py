from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from src.retrieval.vector_store import VECTOR_DB_PATH


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    collection_name="enterprise_knowledge",
    persist_directory=str(VECTOR_DB_PATH),
    embedding_function=embedding_model
)

questions = [
    "How many days of annual leave are provided?",
    "How many sick leave days are available?",
    "How can employees reset their password?",
    "What should employees do when equipment fails?",
    "What is the company's annual bonus amount?",
    "What is the company's maternity leave policy?",
    "Where can I find information about employee promotions?",
    "What is the company's work-from-home policy?"
]

for question in questions:

    print("\nQuestion:", question)

    results = vector_store.similarity_search_with_score(
        question,
        k=3
    )

    for document, score in results:

        source = Path(document.metadata["source"]).name

        print("Source:", source)
        print("Distance score:", round(score, 4))
        print("Content:", document.page_content)
        print("-" * 80)