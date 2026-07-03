# KnowledgeVault

A Retrieval-Augmented Generation (RAG) backend built with FastAPI, Gemini, and Qdrant.

## Features
- Text chunking with overlap
- Gemini embeddings
- Vector similarity search
- Score threshold filtering
- Grounded answer generation

## Tech Stack
- FastAPI
- PostgreSQL / SQLite
- Qdrant
- Google Gemini API
- SQLAlchemy

## Architecture Flow
Text Input
→ Chunk
→ Embed
→ Store in Qdrant

Query
→ Embed
→ Retrieve
→ Gemini Answer

