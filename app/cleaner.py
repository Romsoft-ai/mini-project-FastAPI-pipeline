import pandas as pd
from typing import Dict, Any
from app.fetch_products import load_data
from typing import List , Dict
import os, re, string

def get_dataframe(products: List[Dict]) -> pd.DataFrame:
    """
    Convert a list of product dictionaries into a flat pandas DataFrame.
    Reviews are flattened as r.rating0, r.comment0, r.rating1, etc.
    """
    try:
        if not isinstance(products, list):
            raise ValueError("Input must be a list of product dictionaries.")

        rows = []

        for product in products:
            row = {
                "id": product.get("id"),
                "title": product.get("title"),
                "description": product.get("description"),
                "category": product.get("category"),
                "price": product.get("price"),
                "discountPercentage": product.get("discountPercentage"),
                "rating": product.get("rating"),
                "stock": product.get("stock"),
                "weight": product.get("weight"),
                "width": product.get("dimensions", {}).get("width"),
                "height": product.get("dimensions", {}).get("height"),
                "depth": product.get("dimensions", {}).get("depth"),
                "warrantyInformation": product.get("warrantyInformation"),
                "shippingInformation": product.get("shippingInformation"),
                "availabilityStatus": product.get("availabilityStatus"),
                "returnPolicy": product.get("returnPolicy"),
                "minimumOrderQuantity": product.get("minimumOrderQuantity"),
                "barcode": product.get("meta", {}).get("barcode"),
                "images_link": ", ".join(product.get("images", [])),
                "thumbnail_link": product.get("thumbnail")
            }

            # Flatten all reviews as columns: r.rating0, r.comment0, ...
            reviews = product.get("reviews", [])
            for i, review in enumerate(reviews):
                row[f"r.rating{i}"] = review.get("rating")
                row[f"r.comment{i}"] = review.get("comment")

            rows.append(row)

        return pd.DataFrame(rows)

    except Exception as e:
        print(f"Error generating DataFrame: {e}")
        return pd.DataFrame()


def add_has_return_policy(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")

    df["has_return_policy"] = df["returnPolicy"].apply(
        lambda x: isinstance(x, str) and x.strip().lower() != "no return policy"
    )
    return df

def get_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")

    try:
        summary = (
            df.groupby("category")
            .agg(
                avg_rating=("rating", "mean"),
                min_price=("price", "min"),
                max_price=("price", "max"),
                avg_price=("price", "mean"),
                avg_discount=("discountPercentage", "mean"),
                min_discount=("discountPercentage", "min"),
                max_discount=("discountPercentage", "max"),
            )
            .reset_index()
        )
        return summary
    except Exception as e:
        print(f"Error in category summary: {e}")
        return pd.DataFrame()

def get_cheapest_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Parameter 'n' must be a positive integer.")

    try:
        return df.sort_values(by="price").head(n)[["id", "title", "price", "category", "has_return_policy"]]
    except Exception as e:
        print(f"Error getting cheapest products: {e}")
        return pd.DataFrame()

def get_expensive_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Parameter 'n' must be a positive integer.")

    try:
        return df.sort_values(by="price", ascending=False).head(n)[["id", "title", "price", "category", "has_return_policy"]]
    except Exception as e:
        print(f"Error getting expensive products: {e}")
        return pd.DataFrame()

def prepare_data() -> Dict[str, Any]:
    """
    Main entry point to load data, clean it, generate summary DataFrames.
    Returns a dictionary of results or empty DataFrames on failure.
    """
    try:
        products = load_data()
        if not isinstance(products, list):
            raise ValueError("Data loaded is not a list of products.")

        df = get_dataframe(products)
        df = add_has_return_policy(df)

        category_info_df = get_category_summary(df)
        cheapest_df = get_cheapest_products(df)
        expensive_df = get_expensive_products(df)

        return {
            "df": df,
            "category_info": category_info_df,
            "cheapest": cheapest_df,
            "expensive": expensive_df
        }

    except Exception as e:
        print(f"Failed to prepare data: {e}")
        return {
            "df": pd.DataFrame(),
            "category_info": pd.DataFrame(),
            "cheapest": pd.DataFrame(),
            "expensive": pd.DataFrame()
        }
    

def save_dataframe_to_json(df: pd.DataFrame, output_path: str) -> None:
    """
    Save a pandas DataFrame to a JSON file, ready for MongoDB insertion.
    """
    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_json(output_path, orient="records", indent=4, force_ascii=False)
        print(f"Saved to {output_path}")
    except Exception as e:
        print(f"Error saving DataFrame to JSON: {e}")



def clean_comment_text(text: str) -> str:
    """
    Clean individual comment: lowercase, remove punctuation, normalize spaces.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text



def clean_comments(df: pd.DataFrame, output_path: str = "data/cleaned_comments_data.json") -> pd.DataFrame:
    """
    Extract and clean all comments from review columns using vectorized pandas operations.
    Returns a long-format DataFrame and saves it to JSON.
    """
    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Expected a DataFrame.")
        # extract all columns with comments
        comment_cols = [col for col in df.columns if col.startswith("r.comment")]

        # extraction of comments + some columns
        melted = df[["id", "title", "description", "category"] + comment_cols] \
            .melt(id_vars=["id", "title", "description", "category"],
                  value_vars=comment_cols,
                  var_name="comment_source",
                  value_name="comment")

        # delete lines without comments
        melted = melted[melted["comment"].notna() & melted["comment"].str.strip().ne("")]

        # compute the cleaning using apply()
        melted["cleaned_comment"] = melted["comment"].apply(clean_comment_text)

        # save the results
        save_dataframe_to_json(melted, output_path)

        return melted

    except Exception as e:
        print(f" Error cleaning comments: {e}")
        return pd.DataFrame()






if __name__ == "__main__":
    data = prepare_data()
    if data:
        df = data['df']
        category_info = data['category_info']
        save_dataframe_to_json(category_info, 'data/category_info.json')
        cheapest = data['cheapest']
        save_dataframe_to_json(cheapest,'data/cheapest.json')
        expensive = data['expensive']
        save_dataframe_to_json(expensive, 'data/expensive.json')
        clean_comments(df)
    
