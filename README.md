# Enterprise AI Knowledge Assistant

An intelligent Retrieval-Augmented Generation (RAG) chatbot that helps users retrieve information from enterprise knowledge documents and generate context-aware answers using Large Language Models.

## Project Overview

The Enterprise AI Knowledge Assistant allows users to ask questions about enterprise policies, IT support procedures, and manufacturing operations.

It uses semantic search to retrieve relevant information from a vector database and Google Gemini to generate answers based on the retrieved context.

## Key Features

- Document ingestion and processing
- Text chunking with overlapping segments
- Semantic embeddings using Sentence Transformers
- Vector storage using ChromaDB
- Similarity-based document retrieval
- Context-aware answer generation using Google Gemini
- Source document identification
- Streamlit-based interactive chatbot
- Retrieval evaluation using predefined questions
- Fallback responses when information is unavailable

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| LLM | Google Gemini |
| Framework | LangChain |
| Embeddings | Sentence Transformers |
| Vector Database | ChromaDB |
| Frontend | Streamlit |
| Environment | VS Code, Jupyter Notebook |

## Architecture

User Question
      ↓
Streamlit Chat Interface
      ↓
Question Processing
      ↓
Semantic Search
      ↓
ChromaDB Vector Database
      ↓
Relevant Document Retrieval
      ↓
Context + User Question
      ↓
Google Gemini LLM
      ↓
Generated Answer + Sources

## Project Structure

```text
Enterprise_AI_Knowledge_Assistant/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── processed/
│   └── sample_documents/
│
├── docs/
├── logs/
├── notebooks/
│
├── src/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── chunking/
│   ├── embeddings/
│   ├── retrieval/
│   ├── generation/
│   ├── evaluation/
│   └── utils/
│
├── tests/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.

## Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd Enterprise_AI_Knowledge_Assistant
