"""
Historical price data fetching, backed by Alpha Vantage's free API.
Requires an API key set as the ALPHA_VANTAGE_KEY environment variable.

Supports:
- US stocks (bare ticker, e.g. AAPL, MSFT)
- Indian stocks on BSE (suffix .BSE, e.g. RELIANCE.BSE)
- Crypto (common symbols, e.g. BTC, ETH), priced in USD

Note: free-tier Alpha Vantage only supports "compact" output (~100 most
recent trading days) for stocks. Full history requires a paid plan.
"""

import os
import pandas as pd
import requests

API_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "")

# Common crypto symbols we'll treat as digital currency requests.
CRYPTO_SYMBOLS = {
    "BTC", "ETH", "SOL", "XRP", "ADA", "DOGE", "DOT", "MATIC",
    "LTC", "BCH", "AVAX", "LINK", "UNI", "ATOM", "XLM", "TRX",
}


def _fetch_stock(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    url = (
        "https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_DAILY&symbol={ticker}"
        f"&apikey={API_KEY}&datatype=json"
    )
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()

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
    return df[["Open", "High", "Low", "Close", "Volume"]].astype(float)


def _fetch_crypto(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    url = (
        "https://www.alphavantage.co/query"
        f"?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market=USD"
        f"&apikey={API_KEY}&datatype=json"
    )
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    series = data.get("Time Series (Digital Currency Daily)")
    if not series:
        note = data.get("Note") or data.get("Information") or data.get("Error Message")
        raise ValueError(
            f"No price data found for '{symbol}' in that date range. "
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
    return df[["Open", "High", "Low", "Close", "Volume"]].astype(float)


def fetch_history(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    ticker = (ticker or "").strip().upper()
    if not ticker:
        raise ValueError("Ticker symbol is required.")
    if not API_KEY:
        raise ValueError("Server misconfigured: ALPHA_VANTAGE_KEY is not set.")

    try:
        if ticker in CRYPTO_SYMBOLS:
            df = _fetch_crypto(ticker, start_date, end_date)
        else:
            df = _fetch_stock(ticker, start_date, end_date)
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"Could not fetch data for '{ticker}': {exc}") from exc

    df = df.loc[start_date:end_date]

    if len(df) < 30:
        raise ValueError(
            f"Only {len(df)} trading days of data in that range for '{ticker}' — "
            "too few to backtest meaningfully. Try a wider date range."
        )

    return df