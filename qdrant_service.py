from qdrant_client import QdrantClient, models
import os
from dotenv import load_dotenv
import uuid
load_dotenv()
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
from embeddings import embed_text
client.create_payload_index(
    collection_name="knowledgevault",
    field_name="document_id",
    field_schema=models.PayloadSchemaType.INTEGER,
)
client.create_payload_index(
    collection_name="knowledgevault",
    field_name="user_id",
    field_schema=models.PayloadSchemaType.INTEGER,
)

def store_chunks(doc_id : int, user_id : int, chunks : list[str], embeddings : list[list[float]]):
    points = []
    for chunk_index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        point = {
            "id": str(uuid.uuid4()),
            "vector" : embedding,
            "payload": {
                "user_id" : user_id,
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

def search_chunks(query_embedding: list[float], user_id : int):
    results=client.query_points(
            collection_name="knowledgevault",
            query= query_embedding,
            query_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="user_id",
                            match=models.MatchValue(value=user_id),
                        ),
                    ],
            ),
        )
    chunks = []
    threshold_limit = 0.5
    for point in results.points:
        if point.score < threshold_limit:
            continue
        chunk = point.payload["text"]
        chunks.append(chunk)
    return chunks

def delete_chunks(doc_id : int, user_id: int): #from DOCS
    client.delete(
        collection_name="knowledgevault",
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="document_id",
                        match=models.MatchValue(value=doc_id),
                    ),
                    models.FieldCondition(
                        key="user_id",
                        match=models.MatchValue(value=user_id),
                    ),

                ],
            )
        ),
    )
