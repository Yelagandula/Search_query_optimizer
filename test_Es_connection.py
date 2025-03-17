from elasticsearch import Elasticsearch
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings()

# Connect to Elasticsearch
es = Elasticsearch(
    ["https://localhost:9200"],  # Use https://
    basic_auth=("elastic", "uVBeL99qb*PjSzLXpbyT"),
    verify_certs=False
)

# Define index name
index_name = "search_data"

# Define index mapping
index_mapping = {
    "mappings": {
        "properties": {
            "query": {"type": "text"},
            "rewritten_query": {"type": "text"},
            "results": {
                "type": "nested",
                "properties": {
                    "content": {"type": "text"},
                    "score": {"type": "float"}
                }
            }
        }
    }
}

# Create index (if not exists)
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=index_mapping)
    print(f"Index '{index_name}' created successfully!")
else:
    print(f"Index '{index_name}' already exists!")
