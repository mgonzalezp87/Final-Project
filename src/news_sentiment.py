import requests
import pandas as pd
import json
from datetime import datetime


def fetch_and_aggregate_sentiment(api_key="LURFUTPZ9GZODITP",
        time_from="20230101T0000",
        time_to="20250228T2359",
        topics="economy_macro",
        limit=100,
        output_csv_path=None,
        output_json_path='data/processed/sentiment_raw.json'):
    
    # Fetch and aggregate sentiment data from Alpha Vantage by day

    # Set API endpoint and parameters
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "topics": topics,
        "time_from": time_from,
        "time_to": time_to,
        "limit": limit,
        "apikey": api_key
    }

    # Send GET request to the API
    response = requests.get(url, params)

    # Check if the API response is successful
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    
    # Parse the JSON response
    data = response.json()

    # Optionally save the raw JSON response
    if output_json_path:
        with open(output_json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    
    # Process each article to extract publication date and sentiment
    articles = data.get("feed", [])
    records = []

    for article in articles:
        pub_time_str = article.get("time_published")
        if pub_time_str:
            try:
                pub_date = datetime.strptime(pub_time_str, "%Y%m%dT%H%M%S").date()
                sentiment = float(article.get("overall_sentiment_score", 0))
                records.append({"date": pub_date, "sentiment": sentiment})
            except Exception as e:
                print(f"Error processing an article: {e}")
                
    # Create a DataFrame from the extracted records
    df = pd.DataFrame(records)
    if df.empty:
        print("No sentiment data retrieved.")
        return df

    # Aggregate sentiment data by date
    daily_agg = df.groupby("date").agg(
        avg_sentiment=("sentiment", "mean"),
        article_count=("sentiment", "count")
    ).reset_index()

    # Save aggregated sentiment data to a CSV file if a path is provided
    if output_csv_path:
        daily_agg.to_csv(output_csv_path, index=False)
        print(f"Aggregated sentiment data saved to {output_csv_path}")
    return daily_agg


# Usage
if __name__ == "__main__":
    API_KEY = "LURFUTPZ9GZODITP"
    sentiment_df = fetch_and_aggregate_sentiment(api_key=API_KEY, output_csv_path="data/processed/sentiment_data.csv")
    print("csv saved!!")