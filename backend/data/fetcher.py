"""
Historical price data fetching, backed by Stooq (via pandas-datareader).
No API key is required. Stooq is reliable on cloud hosts, unlike Yahoo
Finance which frequently blocks datacenter IPs.
"""

import pandas as pd
import pandas_datareader.data as web


def fetch_history(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch daily OHLCV history for `ticker` between start_date and end_date
    (both 'YYYY-MM-DD' strings). Raises ValueError on bad input / no data.
    """
    ticker = (ticker or "").strip().upper()
    if not ticker:
        raise ValueError("Ticker symbol is required.")

    try:
        df = web.DataReader(ticker, "stooq", start=start_date, end=end_date)
    except Exception as exc:
        raise ValueError(f"Could not fetch data for '{ticker}': {exc}") from exc

    if df is None or df.empty:
        raise ValueError(
            f"No price data found for '{ticker}' in that date range. "
            "Check the symbol — US tickers are bare (AAPL, MSFT), "
            "NSE tickers need a .NS suffix (RELIANCE.NS), BSE needs .BO, "
            "and London needs .L."
        )

    # Stooq returns data newest-first; sort ascending like yfinance did.
    df = df.sort_index()

    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])

    if len(df) < 30:
        raise ValueError(
            f"Only {len(df)} trading days of data in that range for '{ticker}' — "
            "too few to backtest meaningfully. Try a wider date range."
        )

    return df