from elasticsearch import Elasticsearch
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings()

# Connect to Elasticsearch
es = Elasticsearch(
    ["https://localhost:9200"],
    basic_auth=("elastic", "uVBeL99qb*PjSzLXpbyT"),
    verify_certs=False
)

index_name = "search_data"

def store_query(user_query, rewritten_query, results):
    """
    Store search query & results in Elasticsearch.
    """
    doc = {
        "query": user_query,
        "rewritten_query": rewritten_query,
        "results": results
    }
    res = es.index(index=index_name, body=doc)
    print(f"Stored query: {user_query}, Document ID: {res['_id']}")

# Sample Data
sample_query = "best JavaScript frameworks"
rewritten_query = "top JS frameworks for developers"
sample_results = [
    {"content": "React.js - A UI library by Facebook", "score": 0.95},
    {"content": "Vue.js - A lightweight JS framework", "score": 0.88},
    {"content": "Angular - Google’s framework for enterprise apps", "score": 0.85}
]

# Store in Elasticsearch
store_query(sample_query, rewritten_query, sample_results)
