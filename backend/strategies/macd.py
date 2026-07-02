from typing import Any, Dict

import pandas as pd

from .base import Strategy


class MACDCrossover(Strategy):
    id = "macd_crossover"
    name = "MACD Crossover"

    def generate_signals(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.Series:
        fast = int(params.get("fast_period", 12))
        slow = int(params.get("slow_period", 26))
        signal_period = int(params.get("signal_period", 9))

        ema_fast = df["Close"].ewm(span=fast, adjust=False).mean()
        ema_slow = df["Close"].ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()

        return (macd_line > signal_line).astype(int)
