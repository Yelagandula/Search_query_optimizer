import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys & Configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
