from qdrant_client import QdrantClient, models
import os
from dotenv import load_dotenv
import uuid
from reranker import rerank_chunks
load_dotenv()
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
from embeddings import embed_text
# client.create_payload_index(
#     collection_name="knowledgevault",
#     field_name="document_id",
#     field_schema=models.PayloadSchemaType.INTEGER,
# )
# client.create_payload_index(
#     collection_name="knowledgevault",
#     field_name="user_id",
#     field_schema=models.PayloadSchemaType.INTEGER,
# )

def store_chunks(doc_id : int, user_id : int, chunks : list[str], embeddings : list[list[float]], sparse_embeddings):
    points = []
    for chunk_index, (chunk, embedding, sparse_embedding) in enumerate(zip(chunks, embeddings, sparse_embeddings)):
        point = {
            "id": str(uuid.uuid4()),
            "vector": {
                    "dense": embedding,
                    "sparse": {
                        "indices": sparse_embedding.indices.tolist(),
                        "values": sparse_embedding.values.tolist()
                    }
                },
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

def search_chunks(query_embedding: list[float], query:str, user_id : int, sparse_query):
    sparse_query = models.SparseVector(
        indices=sparse_query.indices.tolist(),
        values=sparse_query.values.tolist()
    )
    results = client.query_points(
        collection_name="knowledgevault",
        prefetch=[
            models.Prefetch(
                query=query_embedding,
                using="dense",
                limit=15,
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="user_id",
                            match=models.MatchValue(value=user_id),
                        ),
                    ],
                ),
            ),
            models.Prefetch(
                query=sparse_query,
                using="sparse",
                limit=15,
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="user_id",
                            match=models.MatchValue(value=user_id),
                        ),
                    ],
                ),
            ),
        ],
    query=models.FusionQuery(
        fusion=models.Fusion.RRF
    ),
        limit = 15,

)
    chunks = []
    for point in results.points:
        chunk = point.payload["text"]
        chunks.append(chunk)
    chunks = rerank_chunks(query, chunks)
    return chunks[:5]

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
