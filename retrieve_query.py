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

def search_query(query):
    """
    Retrieve search results from Elasticsearch.
    """
    es_query = {
        "query": {
            "match": {"query": query}
        }
    }
    
    response = es.search(index=index_name, body=es_query, size=5)
    
    if response["hits"]["hits"]:
        print(f"🔍 Results for '{query}':")
        for hit in response["hits"]["hits"]:
            print(f" - {hit['_source']['rewritten_query']} -> {hit['_source']['results']}")
    else:
        print(f"❌ No results found for '{query}'.")

# Test search query
search_query("best JavaScript frameworks")
