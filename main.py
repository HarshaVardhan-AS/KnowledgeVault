from fastapi import FastAPI, HTTPException, status, Depends
from schemas import DocumentCreate, DocumentResponse, QueryResponse, QueryRequest
import models
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from chunker import chunk_text
from embeddings import embed_text, embed_chunks
from qdrant_service import store_chunks, search_chunks
from llm_service import generate_answer

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/documents", response_model=list[DocumentResponse])
def get_docs(db : Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Document))
    docs = result.scalars().all()
    return docs

@app.get("/documents/{doc_id}", response_model=DocumentResponse)
def get_doc(db: Annotated[Session, Depends(get_db)], doc_id : int):
    result = db.execute(select(models.Document).where(models.Document.id == doc_id))
    doc = result.scalars().first()
    if doc:
        return doc
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

@app.post("/documents/create", response_model=DocumentResponse)
def create_doc(doc : DocumentCreate, db: Annotated[Session, Depends(get_db)]):
    new_doc = models.Document(
        title = doc.title,
        raw_text = doc.raw_text,
        source_type = "text"
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    try:
        chunks = chunk_text(new_doc.raw_text)
        embeddings = embed_chunks(chunks)
        store_chunks(new_doc.id, chunks, embeddings)
    except Exception:
        db.delete(new_doc)
        db.commit()
        raise


    return new_doc


@app.delete("/documents/{doc_id}", status_code = status.HTTP_200_OK)
def delete_doc(doc_id: int, db: Annotated[Session, Depends(get_db)]):
    res = db.execute(select(models.Document).where(models.Document.id == doc_id))
    doc = res.scalars().first()
    if doc:
        db.delete(doc)
        db.commit()
        return {"message" : "Document deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

@app.put("/documents/{doc_id}", response_model=DocumentResponse)
def update_doc(doc: DocumentCreate, doc_id : int, db: Annotated[Session, Depends(get_db)]):
    res = db.execute(select(models.Document).where(models.Document.id == doc_id))
    existing_doc = res.scalars().first()
    if existing_doc:
        existing_doc.title = doc.title
        existing_doc.raw_text = doc.raw_text
        db.commit()
        db.refresh(existing_doc)
        return existing_doc
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

@app.post("/query", response_model=QueryResponse)
def query_docs(request: QueryRequest ):
    query_embedding = embed_text(request.query)
    chunks = search_chunks(query_embedding)
    answer = generate_answer(request.query, chunks)
    return {
        "query" : request.query,
        "chunks" : chunks,
        "answer" : answer
    }

