import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from transformers import AutoTokenizer
from settings import EMBEDDING_MODEL
from src.logs import logger

tokenizer = AutoTokenizer.from_pretrained(
    EMBEDDING_MODEL,
    trust_remote_code=True,
)
import os
os.environ['NLTK_DATA'] = "/Users/yuhsuanting/nltk_data"
nltk.data.path.append(os.environ['NLTK_DATA'])
# nltk.download('punkt', download_dir=os.environ['NLTK_DATA'])
nltk.download("punkt_tab", download_dir=os.environ["NLTK_DATA"])
nltk.download("stopwords", download_dir=os.environ['NLTK_DATA'])
nltk.download("wordnet", download_dir=os.environ['NLTK_DATA'])
# nltk.download(
#     "averaged_perceptron_tagger",
#     download_dir=os.environ["NLTK_DATA"]
# )

def count_tokens(text: str) -> int:
    tokens = tokenizer.encode(text, truncation=False, add_special_tokens=False)
    return len(tokens)

def clean_text(text):
    # Convert text to lowercase
    text = text.lower()

    # # Remove URLs
    # text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)

    # Remove punctuation and special characters
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Tokenization
    tokens = word_tokenize(text)
    # Removing stopwords
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    # Re-join tokens into a string
    clean_text = " ".join(lemmatized_tokens)

    return clean_text

def split_data_chunk(
    embedding_model,
    row_data,
    max_tokens=1048,
    overlap=200,
):
    data = []
    position = 1
    cleaned_text = clean_text(row_data.pop("product_description"))
    title = row_data["title"]
    # Tokenize full_text to IDs
    input_ids = tokenizer.encode(cleaned_text, add_special_tokens=False)
    n = len(input_ids)
    start = 0

    while start < n:
        # logger.debug(f"Processing chunk: {title} part {position}, start: {start}, end: {start + max_tokens}")
        end = min(start + max_tokens, n)
        chunk_ids = input_ids[start:end]
        chunk_text = tokenizer.decode(chunk_ids)

        formatted_text = f"{title} part {position}: {chunk_text}"
        doc_id = f"{row_data['product_id']}_{position}"
        # print("count: ",formatted_text)
        # print(row_data)
        entry = {"product_description": formatted_text, "id": doc_id, **row_data}
        data.append(entry)

        position += 1
        if end == n:
            break  # processed all tokens
        start = max(start + max_tokens - overlap, start + 1)
    # logger.debug(f"Split data chunk: {title} length: {len(data)}")
    # Embed
    texts = [e["product_description"] for e in data]
    embeddings = embedding_model.encode(texts)

    for entry, emb in zip(data, embeddings):
        entry["embedded_product_description"] = emb

    return data
