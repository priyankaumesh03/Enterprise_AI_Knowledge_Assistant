import json
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from src.retrieval.vector_store import VECTOR_DB_PATH


# Project directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load evaluation questions
DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "evaluation_questions.json"

with open(DATASET_PATH, "r", encoding="utf-8") as file:
    evaluation_data = json.load(file)


# Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load existing vector database
vector_store = Chroma(
    collection_name="enterprise_knowledge",
    persist_directory=str(VECTOR_DB_PATH),
    embedding_function=embedding_model
)


# Evaluation counters
correct = 0
total = 0
unknown_questions = 0

print("\n========== RAG RETRIEVAL EVALUATION ==========\n")


for item in evaluation_data:

    question = item["question"]
    expected_source = item["expected_source"]

    print("Question:", question)

    # Unknown questions require a separate answer-generation check
    if expected_source == "unknown":
        unknown_questions += 1
        print("Expected Source: Unknown")
        print("Status: MANUAL ANSWER CHECK")
        print("-" * 60)
        continue

    # Retrieve top 3 relevant documents
    documents = vector_store.similarity_search(
        question,
        k=3
    )

    retrieved_sources = {
        Path(doc.metadata["source"]).name
        for doc in documents
    }

    total += 1

    if expected_source in retrieved_sources:
        correct += 1
        print("Status: PASS")
    else:
        print("Status: FAIL")

    print("Expected Source:", expected_source)
    print("Retrieved Sources:", ", ".join(sorted(retrieved_sources)))
    print("-" * 60)


# Calculate retrieval accuracy
accuracy = (correct / total) * 100 if total else 0

print("\n========== EVALUATION SUMMARY ==========")
print("Total known questions:", total)
print("Correct retrievals:", correct)
print("Incorrect retrievals:", total - correct)
print("Retrieval Accuracy:", f"{accuracy:.2f}%")
print("Unknown questions requiring manual checks:", unknown_questions)
print("========================================")