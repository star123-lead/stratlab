"""
StratLab backend.

Run from inside backend/:
    uvicorn main:app --reload
"""

from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backtest.engine import compute_metrics, run_backtest
from data.fetcher import fetch_history
from strategies import STRATEGY_REGISTRY
from strategies.metadata import STRATEGY_METADATA

app = FastAPI(title="StratLab Backtester")

# Wide open for local development. The Vite dev server proxies /api to this
# server (see frontend/vite.config.ts) so this mainly matters if you ever
# hit the API directly from a different origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class BacktestRequest(BaseModel):
    ticker: str
    strategy_id: str
    params: Dict[str, Any] = Field(default_factory=dict)
    start_date: str
    end_date: str
    initial_capital: float = 10000
    commission_pct: float = 0.1


@app.get("/api/strategies")
def get_strategies():
    return list(STRATEGY_METADATA.values())


@app.post("/api/backtest")
def backtest(req: BacktestRequest):
    if req.strategy_id not in STRATEGY_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Unknown strategy '{req.strategy_id}'.")

    if req.initial_capital <= 0:
        raise HTTPException(status_code=400, detail="Initial capital must be greater than zero.")

    try:
        df = fetch_history(req.ticker, req.start_date, req.end_date)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    strategy = STRATEGY_REGISTRY[req.strategy_id]
    params = req.params if req.params else STRATEGY_METADATA[req.strategy_id]["default_params"]
    signal = strategy.generate_signals(df, params)

    equity_curve, trades = run_backtest(df, signal, req.initial_capital, req.commission_pct)
    metrics = compute_metrics(equity_curve, req.initial_capital, trades)

    bh_strategy = STRATEGY_REGISTRY["buy_hold"]
    bh_signal = bh_strategy.generate_signals(df, {})
    bh_curve, bh_trades = run_backtest(df, bh_signal, req.initial_capital, req.commission_pct)
    bh_metrics = compute_metrics(bh_curve, req.initial_capital, bh_trades)

    price_data = [
        {"date": d.strftime("%Y-%m-%d"), "close": round(float(c), 2), "in_position": int(signal.loc[d])}
        for d, c in zip(df.index, df["Close"])
    ]

    return {
        "ticker": req.ticker.strip().upper(),
        "strategy_id": req.strategy_id,
        "strategy_name": STRATEGY_METADATA[req.strategy_id]["name"],
        "metrics": metrics,
        "benchmark_metrics": bh_metrics,
        "equity_curve": equity_curve,
        "benchmark_equity_curve": bh_curve,
        "price_data": price_data,
        "trades": trades,
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}
