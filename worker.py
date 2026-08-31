from celery import Celery
from database import SessionLocal
import models
from chunker import chunk_text
from embeddings import embed_chunks, sparse_embed_text
from qdrant_service import store_chunks
from doc_parser import extract_text
import os
from dotenv import load_dotenv
import ssl
load_dotenv()

celery_app = Celery(
    "knowledgevault",
    broker=os.getenv("REDIS_URL")
)
celery_app.conf.update(
    broker_use_ssl={
        'ssl_cert_reqs': ssl.CERT_REQUIRED
    },
    redis_backend_use_ssl={
        'ssl_cert_reqs': ssl.CERT_REQUIRED
    }
)
@celery_app.task
def process_document(document_id, user_id, file_path):

    db = SessionLocal()

    try:
        raw_text = extract_text(file_path)
        document = db.query(models.Document).filter(
            models.Document.id == document_id
        ).first()

        if document is None:
            raise Exception("Document not found")

        document.raw_text = raw_text
        db.commit()

        chunks = chunk_text(raw_text)
        embeddings = embed_chunks(chunks)
        sparse_embeddings = sparse_embed_text(chunks)
        store_chunks(document_id, user_id, chunks, embeddings, sparse_embeddings)

        print(f"Document {document_id} processed successfully")

    except Exception:
        db.rollback()
        document = db.query(models.Document).filter(
            models.Document.id == document_id
        ).first()
        if document:
            db.delete(document)
            db.commit()
        raise

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        db.close()