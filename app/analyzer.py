import pandas as pd
import os
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def load_cleaned_comments(path: str = "data/cleaned_comments_data.json") -> pd.DataFrame:
    """
    Load the cleaned comments from local JSON file into a DataFrame.
    """
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        df = pd.read_json(path)
        return df
    
    except Exception as e:
        print(f"Error loading cleaned comments: {e}")
        return pd.DataFrame()

def classify_sentiment(text: str) -> str:
    """
    Classify the sentiment of a given comment using VADER.
    Returns 'positive', 'neutral' or 'negative'.
    """
    try:
        analyzer = SentimentIntensityAnalyzer()
        score = analyzer.polarity_scores(text)["compound"]
        if score >= 0.05:
            return "positive"
        elif score <= -0.05:
            return "negative"
        else:
            return "neutral"
    except Exception as e:
        print(f"Error classifying sentiment: {e}")
        return "unknown"

def analyze_comments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a 'sentiment' column to the DataFrame based on cleaned_comment.
    """
    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Expected a pandas DataFrame.")
        
        df["sentiment"] = df["cleaned_comment"].apply(classify_sentiment)
        return df
    except Exception as e:
        print(f"Error analyzing comments: {e}")
        return pd.DataFrame()

def save_analyzed_comments(df: pd.DataFrame, output_path: str = "data/analyzed_comments_data.json"):
    """
    Save the DataFrame with sentiment analysis to a JSON file.
    """
    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Expected a pandas DataFrame.")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_json(output_path, orient="records", indent=4, force_ascii=False)
        print(f"Analyzed comments saved to {output_path}")
    except Exception as e:
        print(f"Error saving analyzed comments: {e}")

# Optional script entry point
if __name__ == "__main__":
    df_cleaned = load_cleaned_comments()
    if not df_cleaned.empty:
        df_analyzed = analyze_comments(df_cleaned)
        save_analyzed_comments(df_analyzed)
