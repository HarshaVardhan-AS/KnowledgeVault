# KnowledgeVault

A multi-user Retrieval-Augmented Generation (RAG) backend for document ingestion and semantic question answering, built with FastAPI, PostgreSQL, Gemini, and Qdrant.

## Features

* User registration and authentication
* JWT-based authentication with OAuth2 bearer tokens
* Password hashing and secure credential verification
* User-scoped document access and authorization
* Document ingestion support (TXT, PDF)
* CRUD document management
* Text chunking with overlap
* Google Gemini Embeddings API
* User-scoped vector similarity search
* Score threshold filtering
* Grounded answer generation

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Qdrant Vector Database
* Google Gemini API
* JWT / OAuth2
* Password hashing

## Architecture Flow

### Document Ingestion

Text/Document Input
→ Authenticate User
→ Extract Text
→ Store Metadata in PostgreSQL
→ Chunk
→ Embed
→ Store Chunks in Qdrant with User ID

### Query

Authenticated User
→ Embed Query
→ Filter Qdrant by User ID
→ Semantic Search
→ Retrieve Relevant Chunks
→ Gemini Answer

### Authentication

Login
→ Verify Credentials
→ Generate JWT
→ Client Stores Access Token
→ Attach Bearer Token to Protected Requests
→ FastAPI Validates Token
→ Resolve Authenticated User

## Workflow

1. Register an account and securely store the hashed password.
2. Log in to obtain a JWT access token.
3. Authenticate requests using the JWT bearer token.
4. Upload a TXT or PDF document.
5. The document is parsed and converted to raw text.
6. Text is chunked and embedded using Gemini.
7. Document metadata is stored in PostgreSQL and embeddings are stored in Qdrant with the authenticated user's ID.
8. User queries are embedded and matched only against vectors belonging to the authenticated user.
9. Gemini generates a grounded answer using the retrieved context.

## Getting Started

```bash
git clone ...
cd KnowledgeVault

python -m venv .venv
pip install -r requirements.txt

uvicorn main:app --reload
```

## Future Improvements

* Docker containerization
* DOCX support
* OCR for scanned PDFs
* Multimodal document/image ingestion
* Automated testing
* Improved metadata filtering