from typing import Any, Dict

import numpy as np
import pandas as pd

from .base import Strategy


def _rsi(close: pd.Series, period: int) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)


class RSIMeanReversion(Strategy):
    id = "rsi_reversion"
    name = "RSI Mean Reversion"

    def generate_signals(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.Series:
        period = int(params.get("period", 14))
        oversold = float(params.get("oversold", 30))
        overbought = float(params.get("overbought", 70))

        rsi = _rsi(df["Close"], period)

        signal = pd.Series(0, index=df.index, dtype=int)
        position = 0
        for i in range(len(df)):
            r = rsi.iloc[i]
            if position == 0 and r < oversold:
                position = 1
            elif position == 1 and r > overbought:
                position = 0
            signal.iloc[i] = position
        return signal
