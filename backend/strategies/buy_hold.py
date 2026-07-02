from typing import Any, Dict

import pandas as pd

from .base import Strategy


class BuyAndHold(Strategy):
    id = "buy_hold"
    name = "Buy & Hold"

    def generate_signals(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.Series:
        return pd.Series(1, index=df.index, dtype=int)
