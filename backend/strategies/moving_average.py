from typing import Any, Dict

import pandas as pd

from .base import Strategy


class MovingAverageCrossover(Strategy):
    id = "ma_crossover"
    name = "Moving Average Crossover"

    def generate_signals(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.Series:
        fast = int(params.get("fast_period", 20))
        slow = int(params.get("slow_period", 50))

        fast_ma = df["Close"].rolling(window=fast, min_periods=fast).mean()
        slow_ma = df["Close"].rolling(window=slow, min_periods=slow).mean()

        signal = (fast_ma > slow_ma).astype(int)
        signal[fast_ma.isna() | slow_ma.isna()] = 0
        return signal
