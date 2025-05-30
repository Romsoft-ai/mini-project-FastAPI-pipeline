import json
import os
from pymongo import MongoClient
from typing import List

# Connection config
MONGO_URI = "mongodb://mongodb:27017/"
DB_NAME = "product_analysis"

def connect_to_mongo():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def load_json_file(file_path: str) -> List[dict]:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("Expected a list of documents in JSON.")

        return data

    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return []

def insert_data(collection_name: str, file_path: str):
    try:
        db = connect_to_mongo()
        if db is None:
            return

        collection = db[collection_name]
        data = load_json_file(file_path)

        if data:
            collection.delete_many({})  # clean old entries
            collection.insert_many(data)
            print(f"Inserted {len(data)} records into collection '{collection_name}'")

    except Exception as e:
        print(f"Failed to insert into '{collection_name}': {e}")

# ⬇ Specific insert functions
def insert_products():
    insert_data("products", "data/products.json")

def insert_category_info():
    insert_data("category_info", "data/category_info.json")

def insert_cheapest_products():
    insert_data("cheapest_products", "data/cheapest_products.json")

def insert_expensive_products():
    insert_data("expensive_products", "data/expensive_products.json")

def insert_analyzed_comments():
    insert_data("analyzed_comments", "data/analyzed_comments_data.json")

# Optional script runner
if __name__ == "__main__":
    insert_products()
    insert_category_info()
    insert_cheapest_products()
    insert_expensive_products()
    insert_analyzed_comments()
