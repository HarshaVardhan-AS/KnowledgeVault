from flashrank import Ranker, RerankRequest
ranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2")



def rerank_chunks(query:str, chunks : list[str]):
    passages = [{"text": chunk} for chunk in chunks]
    rerank_request = RerankRequest(
        query=query,
        passages=passages
    )
    results = ranker.rerank(rerank_request)
    return [result["text"] for result in results]

# chunks = [
#     "Paris is the capital of France.",
#     "AI is the simulation of human intelligence.",
#     "AI systems can reason and learn.",
#     "Joe Mama is Gae."
# ]
#
# rerank_chunks("what is Artificial intelligence?", chunks)