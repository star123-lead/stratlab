"""
Historical price data fetching, backed by Alpha Vantage's free API.
Requires an API key set as the ALPHA_VANTAGE_KEY environment variable.
"""

import os
import pandas as pd
import requests

API_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "PYNT7KAMG239SNM5")


def fetch_history(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    ticker = (ticker or "").strip().upper()
    if not ticker:
        raise ValueError("Ticker symbol is required.")
    if not API_KEY:
        raise ValueError("Server misconfigured: ALPHA_VANTAGE_KEY is not set.")

    url = (
        "https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_DAILY&symbol={ticker}"
        f"&outputsize=full&apikey={API_KEY}&datatype=json"
    )

    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        raise ValueError(f"Could not fetch data for '{ticker}': {exc}") from exc

    series = data.get("Time Series (Daily)")
    if not series:
        note = data.get("Note") or data.get("Information") or data.get("Error Message")
        raise ValueError(
            f"No price data found for '{ticker}' in that date range. "
            f"{note or 'Check the symbol and try again.'}"
        )

    df = pd.DataFrame.from_dict(series, orient="index")
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume",
    })
    df = df[["Open", "High", "Low", "Close", "Volume"]].astype(float)

    df = df.loc[start_date:end_date]

    if len(df) < 30:
        raise ValueError(
            f"Only {len(df)} trading days of data in that range for '{ticker}' — "
            "too few to backtest meaningfully. Try a wider date range."
        )

    return df