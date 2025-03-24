import json
import requests
import pandas as pd

def get_bls_data(series_ids, start_year, end_year, registration_key=None):
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    payload = {
        "seriesid": series_ids,
        "startyear": start_year,
        "endyear": end_year,
    }
    if registration_key:
        payload["8f87266236ad4fcd96da61220faab65a"] = registration_key

    headers = {"Content-type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Fetch CPI, Unemployment Rate, PPI, and NFP data.
    series_ids = ["CUUR0000SA0", "LNS14000000", "WPUFD49104", "PAYEMS"]
    start_year = "2016"
    end_year = "2025"
    
    data = get_bls_data(series_ids, start_year, end_year)
    series_data = data.get("Results", {}).get("series", [])
    
    all_data = []
    for series in series_data:
        s_id = series.get("seriesID")
        df = pd.DataFrame(series.get("data", []))
        df["seriesID"] = s_id
        all_data.append(df)
    
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_csv("data/processed/bls_data.csv", index=False)
        print("Data saved to bls_data.csv")
    else:
        print("No series data found")