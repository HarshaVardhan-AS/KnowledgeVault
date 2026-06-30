from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def embed_text(text: str):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    embedding = response.embeddings[0].values
    return embedding

def embed_chunks(chunks: list[str]):
    embeddings = []
    for chunk in chunks:
        embedding = embed_text(chunk)
        embeddings.append(embedding)
    return embeddings

