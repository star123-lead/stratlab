# StratLab — Trading Strategy Backtester

A full-stack app for backtesting common technical trading strategies against
real historical price data, plus a built-in reference guide explaining how
each one works.

**Stack:** FastAPI + pandas + yfinance (backend) · React + TypeScript +
Tailwind + Recharts (frontend, via Vite)

## Features

- Backtest Moving Average Crossover, RSI Mean Reversion, MACD Crossover, and
  Bollinger Bands Reversion, with Buy & Hold run automatically as a benchmark
- Real historical data via Yahoo Finance — no API key, no signup
- Metrics: total return, CAGR, max drawdown, Sharpe ratio, win rate
- Equity curve chart (strategy vs. buy & hold), price chart with buy/sell
  markers, and a full trade log
- Strategy reference guide with entry/exit rules, pros/cons, and ideal
  market conditions

## Setup

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Runs at `http://localhost:8000`. Visit `http://localhost:8000/api/health` to
confirm it's up.

### 2. Frontend

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Runs at `http://localhost:5173` — open that in your browser. The Vite dev
server proxies `/api` requests to the backend, so both need to be running.

## Notes

- Data comes from Yahoo Finance via `yfinance`. For non-US tickers, add the
  exchange suffix: `.NS` for NSE (e.g. `RELIANCE.NS`), `.BO` for BSE, `.L`
  for London.
- The backtest engine uses a deliberately simple v1 rule set: one position
  at a time, fully in or fully out (no partial sizing, shorting, or
  leverage), with a commission percentage applied on both legs of every
  trade. That's a real, stated assumption — not a hidden shortcut.
- Swapping the data source only touches one file: `backend/data/fetcher.py`.

## Extending it

- New strategy: add a class implementing `generate_signals()` in
  `backend/strategies/`, register it in `strategies/__init__.py`, and add
  its guide content to `strategies/metadata.py` — the frontend form and
  guide page pick it up automatically via the `param_definitions` schema.
- Parameter sweeps: run one strategy across a grid of parameter values to
  find the best-performing combination for a given ticker.
- Backtest history: would need persistence — SQLite is the simplest add.
- Multi-asset portfolios instead of a single ticker at a time.
- Risk-based or partial position sizing instead of all-in/all-out.
