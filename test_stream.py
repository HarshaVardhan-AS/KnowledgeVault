import requests

url = "http://127.0.0.1:8000/query"

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3ODgxMjM1Njl9.3ZRaG4fCf6t4yw8g-WBGR0kv1xJ-d-2bwf_TjTk1mBs",
    "Content-Type": "application/json"
}

data = {
    "query": "What does a NIC provide and how does it connect a computer to a network?"
}

with requests.post(url, headers=headers, json=data, stream=True) as response:
    response.raise_for_status()

    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
        if chunk:
            print(chunk, end="", flush=True)