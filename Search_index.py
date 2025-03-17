from elasticsearch import Elasticsearch
from config import ELASTICSEARCH_HOST

# Connect to Elasticsearch
es = Elasticsearch([ELASTICSEARCH_HOST])

def create_index():
    """Create an index for storing search queries if it doesn’t exist."""
    if not es.indices.exists(index="search_data"):
        es.indices.create(
            index="search_data",
            body={
                "mappings": {
                    "properties": {
                        "query": {"type": "text"},
                        "rewritten_query": {"type": "text"},
                        "results": {"type": "nested"}
                    }
                }
            }
        )
        print("Index 'search_data' created successfully.")
    else:
        print("Index already exists.")

if __name__ == "__main__":
    create_index()
