from fastapi import FastAPI, HTTPException, status, Depends, UploadFile, File
from schemas import DocumentCreate, DocumentResponse, QueryResponse, QueryRequest
import models
from typing import Annotated
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from chunker import chunk_text
from embeddings import embed_text, embed_chunks
from qdrant_service import store_chunks, search_chunks, delete_chunks
from llm_service import generate_answer
from doc_parser import extract_text
from routers.auth import router
from routers.auth import get_current_user
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router)


@app.get("/")
def root():
    return {"message": "We ball"}


@app.get("/documents", response_model=list[DocumentResponse])
def get_docs(db : Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]):
    result = db.execute(select(models.Document).where(models.Document.user_id == current_user.id))
    docs = result.scalars().all()
    return docs

@app.get("/documents/{doc_id}", response_model=DocumentResponse)
def get_doc(db: Annotated[Session, Depends(get_db)], doc_id : int, current_user: Annotated[models.User, Depends(get_current_user)]):
    result = db.execute(select(models.Document).where(and_(models.Document.id == doc_id, models.Document.user_id == current_user.id)))
    doc = result.scalars().first()
    if doc:
        return doc
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

@app.post("/documents/create", response_model=DocumentResponse, )
def create_doc(doc : DocumentCreate, db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]):
    new_doc = models.Document(
        title = doc.title,
        raw_text = doc.raw_text,
        source_type = "text",
        user_id = current_user.id
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    try:
        chunks = chunk_text(new_doc.raw_text)
        embeddings = embed_chunks(chunks)
        store_chunks(new_doc.id, current_user.id, chunks, embeddings)
    except Exception:
        db.delete(new_doc)
        db.commit()
        raise


    return new_doc


@app.delete("/documents/{doc_id}", status_code = status.HTTP_200_OK)
def delete_doc(doc_id: int, db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]):

    res = db.execute(select(models.Document).where(and_(models.Document.id == doc_id, models.Document.user_id == current_user.id)))
    doc = res.scalars().first()
    if doc:
        delete_chunks(doc_id, current_user.id)
        db.delete(doc)
        db.commit()
        return {"message" : "Document deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")


@app.put("/documents/{doc_id}", response_model=DocumentResponse)
def update_doc(doc: DocumentCreate, doc_id : int, db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]):
    res = db.execute(select(models.Document).where(and_(models.Document.id == doc_id, models.Document.user_id == current_user.id)))
    existing_doc = res.scalars().first()
    if existing_doc:
        existing_doc.title = doc.title
        existing_doc.raw_text = doc.raw_text
        try:
            delete_chunks(doc_id, current_user.id)
            chunks = chunk_text(doc.raw_text)
            embeddings = embed_chunks(chunks)
            store_chunks(existing_doc.id, current_user.id, chunks, embeddings)
        except Exception:
            db.rollback()
            raise
        db.commit()
        db.refresh(existing_doc)
        return existing_doc
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

@app.post("/query", response_model=QueryResponse)
def query_docs(request: QueryRequest , current_user: Annotated[models.User, Depends(get_current_user)] ):
    query_embedding = embed_text(request.query)
    chunks = search_chunks(query_embedding, current_user.id)
    answer = generate_answer(request.query, chunks)
    return {
        "query" : request.query,
        "chunks" : chunks,
        "answer" : answer
    }

@app.post("/documents/upload", response_model = DocumentResponse)
def upload_document(file : UploadFile, db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]):
    raw_text = extract_text(file)
    new_doc = models.Document(
        title=file.filename,
        raw_text=raw_text,
        source_type="File",
        user_id=current_user.id
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    try:
        chunks = chunk_text(new_doc.raw_text)
        embeddings = embed_chunks(chunks)
        store_chunks(new_doc.id,current_user.id, chunks, embeddings)
    except Exception:
        db.delete(new_doc)
        db.commit()
        raise
    return new_doc

