from fastapi import FastAPI, Query
from elasticsearch import Elasticsearch
import redis
import urllib3
import json

# Suppress SSL warnings
urllib3.disable_warnings()

# Initialize FastAPI app
app = FastAPI()

# Connect to Elasticsearch
es = Elasticsearch(
    ["https://localhost:9200"],
    basic_auth=("elastic", "uVBeL99qb*PjSzLXpbyT"),
    verify_certs=False
)

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

index_name = "search_data"

@app.get("/")
def home():
    return {"message": "Welcome to the Search Optimization API"}

@app.get("/search")
def search(query: str = Query(..., title="User Search Query")):
    """
    API endpoint to handle search queries.
    - Uses Redis cache for quick retrieval.
    - Retrieves search results from Elasticsearch.
    """
    # Check Redis cache first
    cached_results = redis_client.get(query)
    if cached_results:
        return {"query": query, "results": json.loads(cached_results), "source": "cache"}

    # Fetch search results from Elasticsearch
    es_query = {"query": {"match": {"query": query}}}
    response = es.search(index=index_name, body=es_query, size=5)

    if response["hits"]["hits"]:
        results = [{"rewritten_query": hit["_source"]["rewritten_query"], "results": hit["_source"]["results"]}
                   for hit in response["hits"]["hits"]]
        
        # Store results in Redis for faster access next time
        redis_client.setex(query, 3600, json.dumps(results))  # Cache for 1 hour
        return {"query": query, "results": results, "source": "elasticsearch"}
    
    return {"query": query, "message": "No results found."}
