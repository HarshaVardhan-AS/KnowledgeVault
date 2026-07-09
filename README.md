# KnowledgeVault

A Retrieval-Augmented Generation (RAG) backend for document ingestion and semantic question answering, built with FastAPI, Gemini, and Qdrant.

## Features
- Document ingestion support (TXT, PDF)
- CRUD document management
- Text chunking with overlap
- Google Gemini Embeddings API
- Vector similarity search
- Score threshold filtering
- Grounded answer generation

## Tech Stack
- FastAPI
- SQLite
- Qdrant Vector Database
- Google Gemini API
- SQLAlchemy

## Architecture Flow
Text/Document Input
→ Extract Text
→ Store Metadata In SQL
→ Chunk
→ Embed
→ Store in Qdrant

Query
→ Embed Query
→ Semantic Search
→ Retrieve Relevant Chunks
→ Gemini Answer

## Workflow

1. Upload a TXT or PDF document.
2. The document is parsed and converted to raw text.
3. Text is chunked and embedded using Gemini.
4. Embeddings are stored in Qdrant.
5. User queries are embedded and matched against stored vectors.
6. Gemini generates a grounded answer using the retrieved context.

## Getting Started

```bash
git clone ...
cd KnowledgeVault

python -m venv .venv
pip install -r requirements.txt

uvicorn main:app --reload
```

## Future Improvements

- DOCX support
- OCR for scanned PDFs
- Metadata filtering