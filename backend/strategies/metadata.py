"""
Descriptive content for each strategy: what it does, its rules, pros/cons,
and the parameter schema the frontend uses to render input controls. Kept
separate from the signal logic in the strategy classes themselves so the
"reference guide" content has one clear home.
"""

STRATEGY_METADATA = {
    "ma_crossover": {
        "id": "ma_crossover",
        "name": "Moving Average Crossover",
        "short_description": "Goes long when a short-term average price crosses above a long-term average, and exits when it crosses back below.",
        "how_it_works": (
            "A classic trend-following strategy. It tracks two moving averages of the "
            "closing price — a faster one that reacts quickly to recent prices, and a "
            "slower one that reacts gradually. When the fast average rises above the "
            "slow average, it suggests upward momentum is building, so the strategy "
            "buys. When the fast average falls back below the slow average, momentum "
            "has turned down, so it exits."
        ),
        "entry_rule": "Fast moving average crosses above the slow moving average.",
        "exit_rule": "Fast moving average crosses below the slow moving average.",
        "pros": [
            "Simple to understand and fully rule-based",
            "Captures large moves during strong, sustained trends",
            "Easy to tune by adjusting the two period lengths",
        ],
        "cons": [
            "Lags the market — it confirms a trend only after it has already started",
            "Prone to whipsaws (false signals) in sideways or choppy markets",
            "Can give back a meaningful chunk of profit before the exit triggers",
        ],
        "best_conditions": "Strongly trending markets, rising or falling, with relatively low day-to-day noise.",
        "default_params": {"fast_period": 20, "slow_period": 50},
        "param_definitions": [
            {"key": "fast_period", "label": "Fast MA (days)", "default": 20, "min": 2, "max": 100},
            {"key": "slow_period", "label": "Slow MA (days)", "default": 50, "min": 5, "max": 300},
        ],
    },
    "rsi_reversion": {
        "id": "rsi_reversion",
        "name": "RSI Mean Reversion",
        "short_description": "Buys when the Relative Strength Index shows the asset is statistically oversold, sells once it recovers to overbought.",
        "how_it_works": (
            "RSI measures the speed and size of recent price moves on a 0-100 scale. "
            "Low readings (typically under 30) suggest the asset has fallen sharply "
            "enough that it may be due for a bounce. High readings (typically over "
            "70) suggest the opposite. This strategy buys when RSI drops into "
            "oversold territory and holds until RSI climbs into overbought territory, "
            "betting on a reversion toward the recent average rather than a "
            "continued trend."
        ),
        "entry_rule": "RSI drops below the oversold threshold.",
        "exit_rule": "RSI rises above the overbought threshold.",
        "pros": [
            "Performs well in range-bound, sideways markets",
            "Doesn't need a strong directional trend to find opportunities",
            "Thresholds are intuitive to reason about and tune",
        ],
        "cons": [
            "Dangerous in strong trends — an asset can stay 'oversold' for a long time while continuing to fall",
            "Effectively fights the prevailing trend rather than following it",
            "Sensitive to the chosen thresholds and lookback period",
        ],
        "best_conditions": "Range-bound or mean-reverting markets without a strong, persistent trend.",
        "default_params": {"period": 14, "oversold": 30, "overbought": 70},
        "param_definitions": [
            {"key": "period", "label": "RSI Period (days)", "default": 14, "min": 2, "max": 50},
            {"key": "oversold", "label": "Oversold Level", "default": 30, "min": 5, "max": 45},
            {"key": "overbought", "label": "Overbought Level", "default": 70, "min": 55, "max": 95},
        ],
    },
    "macd_crossover": {
        "id": "macd_crossover",
        "name": "MACD Crossover",
        "short_description": "Goes long when MACD momentum turns positive relative to its own signal line, exits when momentum fades.",
        "how_it_works": (
            "MACD is the gap between a fast and a slow exponential moving average of "
            "price. A third line — the signal line — is a smoothed average of MACD "
            "itself. When MACD crosses above its signal line, short-term momentum is "
            "accelerating upward, so the strategy buys. When MACD crosses back below "
            "the signal line, momentum is fading, so it exits. It behaves similarly "
            "to a moving average crossover but reacts a bit faster to momentum "
            "shifts."
        ),
        "entry_rule": "MACD line crosses above the signal line.",
        "exit_rule": "MACD line crosses below the signal line.",
        "pros": [
            "Blends trend and momentum into a single signal",
            "Reacts faster than a plain price-based moving average crossover",
            "Well studied and widely used, so its behavior is well understood",
        ],
        "cons": [
            "Still fundamentally a lagging, moving-average-based indicator",
            "Can whipsaw in choppy or low-momentum markets",
            "Three tunable parameters make it easier to accidentally overfit",
        ],
        "best_conditions": "Markets with identifiable momentum shifts and medium-term directional moves.",
        "default_params": {"fast_period": 12, "slow_period": 26, "signal_period": 9},
        "param_definitions": [
            {"key": "fast_period", "label": "Fast EMA", "default": 12, "min": 2, "max": 50},
            {"key": "slow_period", "label": "Slow EMA", "default": 26, "min": 5, "max": 100},
            {"key": "signal_period", "label": "Signal EMA", "default": 9, "min": 2, "max": 50},
        ],
    },
    "bollinger_reversion": {
        "id": "bollinger_reversion",
        "name": "Bollinger Bands Reversion",
        "short_description": "Buys when price falls below its lower volatility band, expecting a reversion back toward the average.",
        "how_it_works": (
            "Bollinger Bands plot a moving average of price together with an upper "
            "and lower band set a chosen number of standard deviations away, so the "
            "bands automatically widen when volatility rises and narrow when it "
            "falls. When price closes below the lower band, it's statistically "
            "stretched to the downside, so the strategy buys, expecting a reversion "
            "toward the middle band. It exits once price recovers back to the middle "
            "band."
        ),
        "entry_rule": "Price closes below the lower Bollinger Band.",
        "exit_rule": "Price closes back above the middle band (the moving average).",
        "pros": [
            "Automatically adapts to changing volatility",
            "Works well on range-bound, mean-reverting assets",
            "Visually intuitive — the bands map directly onto a price chart",
        ],
        "cons": [
            "In a strong downtrend, price can 'ride' the lower band for a long time before reverting",
            "Like other mean-reversion strategies, it fights the prevailing trend",
            "The standard deviation multiplier meaningfully changes signal frequency",
        ],
        "best_conditions": "Range-bound, volatile-but-non-trending markets.",
        "default_params": {"period": 20, "std_dev": 2},
        "param_definitions": [
            {"key": "period", "label": "Period (days)", "default": 20, "min": 5, "max": 100},
            {"key": "std_dev", "label": "Std. Deviations", "default": 2, "min": 1, "max": 4},
        ],
    },
    "buy_hold": {
        "id": "buy_hold",
        "name": "Buy & Hold",
        "short_description": "Buys on day one and holds for the entire period — the baseline every active strategy is measured against.",
        "how_it_works": (
            "No active decisions are made after the initial purchase: the full "
            "position is bought at the start of the date range and held, unchanged, "
            "until the end. It's included primarily as a benchmark, since every "
            "other strategy here is compared against it automatically in the results."
        ),
        "entry_rule": "Start of the selected date range.",
        "exit_rule": "End of the selected date range.",
        "pros": [
            "Zero trading costs beyond the single initial purchase",
            "Captures the full benefit of long-term growth with no risk of mistimed entries or exits",
            "Historically difficult to beat over long horizons for broad indices and strong companies",
        ],
        "cons": [
            "Fully exposed to every drawdown along the way, with no downside protection",
            "Entirely passive — provides no edge if the asset is genuinely overvalued",
        ],
        "best_conditions": "Used here as the yardstick for whether an active strategy actually adds value.",
        "default_params": {},
        "param_definitions": [],
    },
}
