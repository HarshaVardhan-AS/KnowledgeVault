from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def generate_answer(query: str, chunks: list[str]):
    context = "\n\n".join(chunks)
    prompt = f"""
    You are a helpful assistant.

    Answer the user's question using ONLY the context below.

    Context:
    {context}

    Question:
    {query}

    If the answer is not in the context, say that the information is not available.
    """
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    return response.text

