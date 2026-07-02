"""
Trade simulation and performance metrics.

Deliberately simple v1 rules: a single position at a time, fully in or
fully out (no partial sizing, no shorting, no leverage), with a commission
percentage applied on both the buy and the sell leg of every trade. That's
a real assumption set, not a hidden shortcut — see the README for ideas on
extending it.
"""

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


def run_backtest(
    df: pd.DataFrame,
    in_position: pd.Series,
    initial_capital: float,
    commission_pct: float = 0.1,
) -> Tuple[List[dict], List[dict]]:
    cash = float(initial_capital)
    shares = 0.0
    position_open = False
    entry_price = 0.0
    entry_date = None
    cash_before_trade = 0.0

    trades: List[dict] = []
    equity_records: List[dict] = []

    for date, row in df.iterrows():
        price = float(row["Close"])
        signal = int(in_position.loc[date])

        if signal == 1 and not position_open:
            cash_before_trade = cash
            commission = cash * (commission_pct / 100.0)
            investable = max(cash - commission, 0.0)
            shares = investable / price if price > 0 else 0.0
            cash = 0.0
            position_open = True
            entry_price = price
            entry_date = date

        elif signal == 0 and position_open:
            proceeds = shares * price
            commission = proceeds * (commission_pct / 100.0)
            cash = proceeds - commission
            pnl = cash - cash_before_trade
            return_pct = (cash / cash_before_trade - 1) * 100 if cash_before_trade > 0 else 0.0
            trades.append({
                "entry_date": entry_date.strftime("%Y-%m-%d"),
                "exit_date": date.strftime("%Y-%m-%d"),
                "entry_price": round(entry_price, 2),
                "exit_price": round(price, 2),
                "shares": round(shares, 4),
                "pnl": round(pnl, 2),
                "return_pct": round(return_pct, 2),
            })
            shares = 0.0
            position_open = False

        portfolio_value = cash + shares * price
        equity_records.append({"date": date.strftime("%Y-%m-%d"), "value": round(portfolio_value, 2)})

    return equity_records, trades


def compute_metrics(equity_records: List[dict], initial_capital: float, trades: List[dict]) -> Dict[str, float]:
    if not equity_records:
        return {
            "total_return_pct": 0.0, "cagr_pct": 0.0, "max_drawdown_pct": 0.0,
            "sharpe_ratio": 0.0, "win_rate_pct": 0.0, "num_trades": 0,
            "final_value": round(initial_capital, 2),
        }

    s = pd.Series(
        data=[r["value"] for r in equity_records],
        index=pd.to_datetime([r["date"] for r in equity_records]),
    )

    final_value = float(s.iloc[-1])
    total_return_pct = (final_value / initial_capital - 1) * 100 if initial_capital > 0 else 0.0

    days = (s.index[-1] - s.index[0]).days
    years = days / 365.25
    if years > 0 and final_value > 0 and initial_capital > 0:
        cagr_pct = ((final_value / initial_capital) ** (1 / years) - 1) * 100
    else:
        cagr_pct = 0.0

    running_max = s.cummax()
    drawdown = (s - running_max) / running_max.replace(0, np.nan)
    max_drawdown_pct = float(drawdown.min() * 100) if not drawdown.empty else 0.0
    if np.isnan(max_drawdown_pct):
        max_drawdown_pct = 0.0

    daily_returns = s.pct_change().dropna()
    if len(daily_returns) > 1 and daily_returns.std() > 0:
        sharpe_ratio = float((daily_returns.mean() / daily_returns.std()) * np.sqrt(252))
    else:
        sharpe_ratio = 0.0

    wins = [t for t in trades if t["pnl"] > 0]
    win_rate_pct = (len(wins) / len(trades) * 100) if trades else 0.0

    return {
        "total_return_pct": round(total_return_pct, 2),
        "cagr_pct": round(cagr_pct, 2),
        "max_drawdown_pct": round(max_drawdown_pct, 2),
        "sharpe_ratio": round(sharpe_ratio, 2),
        "win_rate_pct": round(win_rate_pct, 2),
        "num_trades": len(trades),
        "final_value": round(final_value, 2),
    }
