from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv
import uuid
load_dotenv()
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
from embeddings import embed_text

def store_chunks(doc_id : int, chunks : list[str], embeddings : list[list[float]]):
    points = []
    for chunk_index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        point = {
            "id": str(uuid.uuid4()),
            "vector" : embedding,
            "payload": {
                "document_id": doc_id,
                "chunk_index": chunk_index,
                "text": chunk
            }
        }
        points.append(point)

    try:
        client.upsert(
            collection_name="knowledgevault",
            points=points
        )
    except Exception as e:
        raise e

def search_chunks(query_embedding: list[float]):
    results = client.query_points(
            collection_name="knowledgevault",
            query=query_embedding,
            limit=3
    )
    chunks = []
    threshold_limit = 0.5
    for point in results.points:
        if point.score < threshold_limit:
            continue
        chunk = point.payload["text"]
        chunks.append(chunk)
    return chunks

