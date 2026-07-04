"""
Historical price data fetching, backed directly by Stooq's CSV endpoint.
No API key is required. Stooq is reliable on cloud hosts, unlike Yahoo
Finance which frequently blocks datacenter IPs.
"""

import pandas as pd
import requests
import io


def fetch_history(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch daily OHLCV history for `ticker` between start_date and end_date
    (both 'YYYY-MM-DD' strings). Raises ValueError on bad input / no data.
    """
    ticker = (ticker or "").strip().upper()
    if not ticker:
        raise ValueError("Ticker symbol is required.")

    stooq_symbol = ticker.lower()
    if "." not in stooq_symbol:
        stooq_symbol += ".us"

    d1 = start_date.replace("-", "")
    d2 = end_date.replace("-", "")

    url = f"https://stooq.com/q/d/l/?s={stooq_symbol}&d1={d1}&d2={d2}&i=d"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        print(f"[STOOQ DEBUG] URL: {url}")
        print(f"[STOOQ DEBUG] Status: {resp.status_code}")
        print(f"[STOOQ DEBUG] First 300 chars: {resp.text[:300]}")
        resp.raise_for_status()
        df = pd.read_csv(io.StringIO(resp.text))
    except Exception as exc:
        raise ValueError(f"Could not fetch data for '{ticker}': {exc}") from exc

    if df is None or df.empty or "Date" not in df.columns:
        raise ValueError(
            f"No price data found for '{ticker}' in that date range. "
            "Check the symbol — US tickers are bare (AAPL, MSFT), "
            "NSE tickers need a .NS suffix (RELIANCE.NS), BSE needs .BO, "
            "and London needs .L."
        )

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date").sort_index()

    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])

    if len(df) < 30:
        raise ValueError(
            f"Only {len(df)} trading days of data in that range for '{ticker}' — "
            "too few to backtest meaningfully. Try a wider date range."
        )

    return df