# 🧠  FastAPI Data Pipeline

This project is a complete **Data Engineering pipeline** built with **FastAPI**, **MongoDB**, and **Docker**. It covers all the stages from data collection to processing, analysis, and persistence, wrapped in a modular and API-accessible application.

---

## 📌 Project Description

This application performs the following key steps:

1. **Data Collection**: Fetches product data from the [DummyJSON API](https://dummyjson.com/products).
2. **Data Cleaning**: Transforms and cleans product information and review comments.
3. **Analysis**:
   - Generates summary insights per product category.
   - Extracts cheapest and most expensive products.
   - Analyzes the sentiment of product review comments.
4. **Storage**: Saves the processed data into a MongoDB database.
5. **API Access**: Exposes endpoints via FastAPI to trigger each pipeline phase.

---

## ⚙️ Technologies Used

- **FastAPI** — API framework for serving the pipeline
- **MongoDB** — NoSQL database to store all structured and processed data
- **Docker / Docker Compose** — For full containerization of the application
- **Pandas** — Data transformation and statistical analysis
- **VADER Sentiment** — Rule-based sentiment analysis on product reviews
- **Uvicorn** — ASGI server for running FastAPI
- **Python 3.10+**

---

## 🚀 How to Run the Project (with Docker)

> Make sure Docker and Docker Compose are installed on your machine.

### 1. Clone the repository 

```bash
git clone https://github.com/your-username/asphere-fastapi-pipeline.git
cd mini-project-FastAPI-pipeline
```
### 2. Build and starts the conteneur

```bash
docker-compose up build
```
### Access the API 

Visit http://localhost:8000/docs to explore the Swagger UI and test the endpoints.

### API end-points

/category-summary	Generate summary per product category
/product-extremes	Extract cheapest and most expensive products
/analyze-comments	Clean and analyze sentiment of product reviews

### Sample MongoDB Collections

Once pipelines are executed, data will be saved to MongoDB under:

    products

    category_info

    cheapest_products

    expensive_products

    analyzed_comments

> You can explore the database using MongoDB Compass or CLI.

### Author
Albert Romuald Noubissi - Data Engineer | FastAPI & AI Enthusiast
linkedin: https://www.linkedin.com/in/noubissi-romuald-albert-71b4801b7/
