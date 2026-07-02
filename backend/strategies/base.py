"""Shared interface every strategy implements."""

from abc import ABC, abstractmethod
from typing import Any, Dict

import pandas as pd


class Strategy(ABC):
    id: str = "base"
    name: str = "Base Strategy"

    @abstractmethod
    def generate_signals(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.Series:
        """
        Return a 0/1 integer Series aligned with df.index:
        1 = should be holding a position that day, 0 = should be in cash.

        The backtest engine treats every 0->1 transition as a buy and every
        1->0 transition as a sell, so strategies only need to decide
        "in or out", not place orders themselves.
        """
        raise NotImplementedError
