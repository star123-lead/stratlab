"""
Strategy registry. To add a new strategy: write a class implementing
Strategy.generate_signals() in its own file, then register it here and add
its descriptive content to metadata.py.
"""

from .bollinger import BollingerBandsReversion
from .buy_hold import BuyAndHold
from .macd import MACDCrossover
from .moving_average import MovingAverageCrossover
from .rsi import RSIMeanReversion

STRATEGY_REGISTRY = {
    "ma_crossover": MovingAverageCrossover(),
    "rsi_reversion": RSIMeanReversion(),
    "macd_crossover": MACDCrossover(),
    "bollinger_reversion": BollingerBandsReversion(),
    "buy_hold": BuyAndHold(),
}
