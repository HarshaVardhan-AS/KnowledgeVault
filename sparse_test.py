from fastembed import SparseTextEmbedding

model = SparseTextEmbedding(model_name="Qdrant/bm25")

documents = [
    "Artificial intelligence is the simulation of human intelligence.",
    "AI systems can reason and learn.",
    "Paris is the capital of France.",
]

embeddings = list(model.embed(documents))

for embedding in embeddings:
    print(embedding)