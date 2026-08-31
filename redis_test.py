import json
import redis

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

job = redis_client.lpop("ingestion_queue")
print(redis_client.lrange("ingestion_queue", 0, -1))

print(json.loads(job))