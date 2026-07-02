from typing import Any, Dict

import pandas as pd

from .base import Strategy


class BollingerBandsReversion(Strategy):
    id = "bollinger_reversion"
    name = "Bollinger Bands Reversion"

    def generate_signals(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.Series:
        period = int(params.get("period", 20))
        std_dev = float(params.get("std_dev", 2))

        sma = df["Close"].rolling(window=period, min_periods=period).mean()
        std = df["Close"].rolling(window=period, min_periods=period).std()
        lower_band = sma - std_dev * std

        signal = pd.Series(0, index=df.index, dtype=int)
        position = 0
        for i in range(len(df)):
            close = df["Close"].iloc[i]
            mid = sma.iloc[i]
            lower = lower_band.iloc[i]
            if pd.isna(mid) or pd.isna(lower):
                signal.iloc[i] = position
                continue
            if position == 0 and close < lower:
                position = 1
            elif position == 1 and close > mid:
                position = 0
            signal.iloc[i] = position
        return signal
