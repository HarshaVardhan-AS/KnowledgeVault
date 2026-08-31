# KnowledgeVault

A multi-user hybrid Retrieval-Augmented Generation (RAG) backend for document ingestion and grounded question answering, built with FastAPI, Qdrant Cloud, Google Gemini, Celery, and Upstash Redis.

## Features

* User registration and authentication
* JWT-based authentication with OAuth2 bearer tokens
* Password hashing and secure credential verification
* User-scoped document access and vector isolation
* Document ingestion support (TXT, PDF)
* CRUD document management
* Asynchronous document ingestion using Celery
* Upstash Redis-backed task queue
* Two-stage document extraction with native parsing and EasyOCR fallback
* Text chunking with overlap
* 3072-dimensional Google Gemini dense embeddings
* BM25 sparse embeddings using FastEmbed
* Hybrid dense + sparse retrieval
* Reciprocal Rank Fusion (RRF)
* User-scoped vector similarity search
* FlashRank cross-encoder reranking
* Score threshold filtering
* Grounded answer generation using Google Gemini
* Real-time response streaming

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Qdrant Cloud
* Google Gemini API
* FastEmbed
* FlashRank
* Celery
* Upstash Redis
* JWT / OAuth2
* EasyOCR
* pypdfium2
* Password hashing


### Document Ingestion

Document Upload
→ Authenticate User
→ Create Document Metadata
→ Queue Celery Task
→ Extract Text
→ Native Parsing
→ EasyOCR Fallback (if required)
→ Chunk Text
→ Generate Dense + Sparse Embeddings
→ Store Chunks in Qdrant with User ID

### Query

Authenticated User
→ Generate Dense Query Embedding
→ Generate Sparse BM25 Query Embedding
→ Filter by User ID
→ Dense Retrieval
→ Sparse Retrieval
→ Reciprocal Rank Fusion (RRF)
→ FlashRank Reranking
→ Retrieve Top Context
→ Gemini Grounded Generation
→ Stream Response

### Authentication

Login
→ Verify Credentials
→ Generate JWT
→ Client Stores Access Token
→ Attach Bearer Token to Protected Requests
→ FastAPI Validates Token
→ Resolve Authenticated User

## Retrieval Pipeline

KnowledgeVault uses a hybrid retrieval pipeline combining semantic and lexical search.

1. The user's query is embedded using Google's Gemini embedding model to produce a 3072-dimensional dense vector.
2. The same query is converted into a sparse BM25 representation using FastEmbed.
3. Dense and sparse searches independently retrieve candidate chunks from Qdrant.
4. Results are fused using Reciprocal Rank Fusion (RRF).
5. The fused candidates are reranked using FlashRank's cross-encoder.
6. The highest-ranked chunks are passed to Gemini as grounded context.

## Asynchronous Ingestion

Document processing is handled asynchronously using Celery and Upstash Redis.

Instead of performing document extraction and processing directly inside the API request:

1. The API authenticates the user and creates the document record.
2. A Celery task is queued through Upstash Redis.
3. The worker performs document extraction, OCR fallback, chunking, and embedding.
4. Processed chunks are stored in Qdrant.

This prevents expensive document processing from blocking the API request cycle.

## Grounded Generation

Generated answers are explicitly instructed to use only the retrieved document context.

If the retrieved context does not contain enough information to answer the question, the system responds that the information is not available rather than relying on unrelated model knowledge.

Responses are streamed incrementally using FastAPI's `StreamingResponse` and Gemini's streaming generation API.

## Getting Started

### Prerequisites

* Python 3.13
* Qdrant Cloud account
* Google Gemini API key
* Upstash Redis database

### Installation

```bash
git clone https://github.com/HarshaVardhan-AS/KnowledgeVault.git
cd KnowledgeVault

python -m venv .venv
```

Activate the virtual environment:

**Windows:**

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_database_url
UPSTASH_REDIS_REST_URL=your_upstash_redis_url
UPSTASH_REDIS_REST_TOKEN=your_upstash_redis_token
```

### Run the API

```bash
uvicorn main:app --reload
```

### Run the Celery Worker

In a separate terminal:

```bash
celery -A worker.celery worker --loglevel=info -P solo
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Future Improvements

* Docker containerization
* DOCX support
* Multimodal document and image ingestion
* Automated testing
* Improved metadata filtering
* Production deployment