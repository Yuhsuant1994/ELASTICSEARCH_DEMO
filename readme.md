# Elasticsearch

## prerequisite

1. install docker desktop
2. refer to [official guide](https://www.elastic.co/docs/deploy-manage/deploy/self-managed/install-elasticsearch-docker-compose) to setup elasticsearch server 

## dataset

1. get Nike product data from kaggle [link](https://www.kaggle.com/datasets/adwaitkesharwani/nike-product-descriptions)
2. create fake product ID to the dataset
    ```
    import random, string
    import pandas as pd
    from settings import INPUT_DATA_PATH
    def generate_product_id(length=10):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=length))
    df = pd.read_csv(INPUT_DATA_PATH)
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df['product_id'] = [generate_product_id() for _ in range(len(df))]
    df.to_csv(INPUT_DATA_PATH, index=False)
    ```