import requests
import json
import os
from typing import Union, List


def fetch_all_products(batch_size: int = 100) -> Union[List[dict], None]:
    """
    Fetch all products from the DummyJSON API using pagination.
    Returns a list of product dictionaries or None if an error occurs.

    based on the number of produts available on the dummyJson site, the batch_size can easily be 
    ajusted.
    """
    try:
        if not isinstance(batch_size, int) or batch_size <= 0:
            raise ValueError("batch_size must be a positive integer.")

        all_products = []
        skip = 0
        total = None

        while True:
            url = f"https://dummyjson.com/products?limit={batch_size}&skip={skip}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            if "products" not in data:
                raise ValueError("Invalid API response: missing 'products'.")

            products = data["products"]
            all_products.extend(products)

            if total is None:
                total = data.get("total", len(products))

            skip += batch_size
            if skip >= total:
                break

        print(f"Successfully fetched {len(all_products)} products.")
        return all_products

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except ValueError as ve:
        print(f"Invalid input or response: {ve}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None


def save_data(data: Union[List[dict], dict], output_path: str =  "data/products.json") -> None: 
    """
    Save data (list or dict) to a JSON file locally.
    By default the data is save locally to 'data/products.json'
    If the user provide a custom output_path then the data will be saved to the provided custom path
    """
    try:
        if not isinstance(data, (dict, list)) or not isinstance(output_path, str):
            raise ValueError("Data must be a dictionary/list or make sure the output_path is a str.")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Data saved to {output_path}")
    except Exception as e:
        print(f"Error saving data: {e}")


def load_data(input_path: str = "data/products.json") -> Union[dict, List[dict], None]:
    """
    Load product data from a local JSON file.
    Th fonction return either a dict, a list of dict or None if an error occurs.
    Read data from default local path_file 'data/products.json'
    """
    try:
        if not isinstance(input_path, str):
            raise ValueError("The input_file must be a str")
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"File not found: {input_path}")

        with open(input_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:
        print(f"Error loading data: {e}")
        return None


# Optionnel : pour tester en direct
if __name__ == "__main__":
    products = fetch_all_products()
    saved = 1 # saved takes 1 if the data has already been saved
    if products and not saved:
        save_data(products)
        loaded = load_data()
        print(f" Loaded {len(loaded)} products from file.")
    elif products and saved: 
        loaded = load_data() 
        print(f" Loaded {len(loaded)} products from file.")

