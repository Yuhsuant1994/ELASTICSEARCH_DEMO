import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
from src.logs import logger
# Load .env file
load_dotenv()


class ES_HELPER:
    def __init__(self):
        username = os.getenv("ES_USER")
        password = os.getenv("ES_PASSWORD")
        host = os.getenv("ES_HOST", "")
        logger.info(host)
        self.client = Elasticsearch(
            hosts=host,
            basic_auth=(username, password),
            ssl_show_warn=False,
            verify_certs=False,
        )

    def is_index_exists(self, index_name: str):
        if not index_name:
            return False
        return self.client.indices.exists(index=index_name)

    def _delete_index(self, name):
        logger.info(f"index {name} deleted")
        return self.client.indices.delete(index=name)

    def create_index(
        self,
        index_name: str,
    ):
        settings_and_mappings = self.get_index_dsl()
        response = self.client.indices.create(
            index=index_name,
            body=settings_and_mappings,
        )
        logger.info(response)
        return response

    def doc_generator(self, data, index_name: str):
        for item in data:
            # logger.info(item)
            document = {
                "_index": index_name,
                "_id": item.pop("id"),
                "_source": item,
            }
            yield document

    def update_data(self, data, index_name) -> None:
        for success, info in helpers.parallel_bulk(
            client=self.client,
            actions=self.doc_generator(data, index_name),
            thread_count=4,
            chunk_size=500,
            max_chunk_bytes=104857600,
            queue_size=4,
            refresh="true",
        ):
            if not success:
                logger.info("A document failed:", info)
                
    def get_index_dsl(self):
        return {
            "settings": {
                "analysis": {
                    "filter": {
                        "synonym_filter": {
                            "type": "synonym",
                            "synonyms_path": "synonyms.txt"
                        }
                    },
                    "analyzer": {
                        "custom_analyzer": {
                            "tokenizer": "standard",
                            "filter": ["lowercase", "synonym_filter"],
                        }
                    }
                },
            },
            "mappings": {
                "properties": {
                    "product_id": {"type": "keyword"},
                    "title": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword"}},
                    },
                    "subtitle": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword"}},
                    },
                    "product_description": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword"}},
                    },
                    "embedded_product_description": {
                        "type": "dense_vector",
                        "dims": 768,
                        "index": True,
                        "similarity": "cosine",
                    }
                }
            },
        }


    # def update_data(self, data):

    # # Step 1: Read the CSV file
    # file_path = 'data/customer_churn.csv'  # Replace with your CSV file path
    # dataframe = pd.read_csv(file_path)

    # # Step 2: Connect to Elasticsearch
    # # Step 3: Prepare and Index the Data
    # def generate_data(df):
    #     for index, row in df.iterrows():
    #         yield {
    #             "_index": "customer_churn",  # Replace with your index name
    #             "_id": index,
    #             "_source": row.to_dict(),
    #         }

    # # Indexing data to Elasticsearch
    # helpers.bulk(client, generate_data(dataframe))