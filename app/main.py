from fastapi import FastAPI
from app.cleaner import prepare_data, clean_comments, save_dataframe_to_json
from app.analyzer import load_cleaned_comments, analyze_comments, save_analyzed_comments
from app.database import (
    insert_category_info,
    insert_cheapest_products,
    insert_expensive_products,
    insert_analyzed_comments
)

app = FastAPI(title="Product Analytics API")

@app.get("/")
def home():
    return {"message": "Welcome to the Product Analytics API 🚀"}

@app.get("/category-summary")
def category_summary():
    try:
        result = prepare_data()
        category_df = result["category_info"]
        save_dataframe_to_json(category_df, "data/category_info.json")
        insert_category_info()
        return {"message": "Category summary inserted into MongoDB"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/product-extremes")
def product_extremes():
    try:
        result = prepare_data()
        cheapest = result["cheapest"]
        expensive = result["expensive"]
        save_dataframe_to_json(cheapest, "data/cheapest_products.json")
        save_dataframe_to_json(expensive, "data/expensive_products.json")
        insert_cheapest_products()
        insert_expensive_products()
        return {"message": " Cheapest and most expensive products inserted into MongoDB"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/analyze-comments")
def analyze_comments_endpoint():
    try:
        result = prepare_data()
        df = result["df"]
        cleaned_df = clean_comments(df)
        analyzed_df = analyze_comments(cleaned_df)
        save_analyzed_comments(analyzed_df)
        insert_analyzed_comments()
        return {"message": "Comments analyzed and inserted into MongoDB"}
    except Exception as e:
        return {"error": str(e)}
