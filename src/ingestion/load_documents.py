from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader


# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Define the sample documents folder
DOCUMENTS_PATH = PROJECT_ROOT / "data" / "sample_documents"


def load_documents():

    print("Loading documents...")

    loader = DirectoryLoader(
        str(DOCUMENTS_PATH),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True
    )

    documents = loader.load()

    print(f"\nTotal documents loaded: {len(documents)}")

    for document in documents:
        print("\nDocument:", Path(document.metadata["source"]).name)
        print("Characters:", len(document.page_content))

    return documents


if __name__ == "__main__":
    load_documents()