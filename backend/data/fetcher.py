"""
Historical price data fetching, backed by Yahoo Finance via the `yfinance`
library. No API key is required.

Kept isolated in this one module on purpose: if you ever want to swap in a
different provider (Alpha Vantage, Twelve Data, Polygon, etc.), this is the
only file that needs to change. Everything downstream just expects a
DataFrame indexed by date with Open/High/Low/Close/Volume columns.
"""

import pandas as pd
import yfinance as yf


def fetch_history(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch daily OHLCV history for `ticker` between start_date and end_date
    (both 'YYYY-MM-DD' strings). Raises ValueError on bad input / no data.
    """
    ticker = (ticker or "").strip().upper()
    if not ticker:
        raise ValueError("Ticker symbol is required.")

    try:
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date, interval="1d")
    except Exception as exc:  # network / yfinance internals
        raise ValueError(f"Could not fetch data for '{ticker}': {exc}") from exc

    if df is None or df.empty:
        raise ValueError(
            f"No price data found for '{ticker}' in that date range. "
            "Check the symbol — US tickers are bare (AAPL, MSFT), "
            "NSE tickers need a .NS suffix (RELIANCE.NS), BSE needs .BO, "
            "and London needs .L."
        )

    # yfinance can return a tz-aware index; normalize to naive dates so it
    # serializes cleanly and compares predictably everywhere downstream.
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)

    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])

    if len(df) < 30:
        raise ValueError(
            f"Only {len(df)} trading days of data in that range for '{ticker}' — "
            "too few to backtest meaningfully. Try a wider date range."
        )

    return df
