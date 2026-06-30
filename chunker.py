def chunk_text(raw_text: str) -> list[str]:
    chunks = []
    chunk_size = 500
    overlap = 100
    start = 0
    while start < len(raw_text):
        raw_chunk = raw_text[start:start + chunk_size]
        chunks.append(raw_chunk)
        start+= chunk_size - overlap
    return chunks


