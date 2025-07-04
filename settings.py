import os


PROJECT_NAME = "ES_DEMO"
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw")
RAW_DATA_PATH = os.path.join(DATA_PATH, "raw_data")
LOG_PATH = os.path.join(DATA_PATH, "logs")
INPUT_DATA_PATH = os.path.join(DATA_PATH, "NikeProductDescriptions.csv")

EMBEDDING_MODEL = 'sentence-transformers/all-mpnet-base-v2'
# EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1.5"
INDEX_NAME = "nike_product"