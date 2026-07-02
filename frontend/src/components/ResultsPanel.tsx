import type { BacktestResult } from '../types'
import EquityChart from './EquityChart'
import MetricCards from './MetricCards'
import PriceChart from './PriceChart'
import TradeLog from './TradeLog'

export default function ResultsPanel({ result }: { result: BacktestResult }) {
  const firstDate = result.price_data[0]?.date
  const lastDate = result.price_data[result.price_data.length - 1]?.date

  return (
    <div className="space-y-6">
      <div>
        <h2 className="font-display font-semibold text-lg">
          {result.strategy_name}
          <span className="text-paper/40 font-normal"> on </span>
          <span className="text-amber tracking-wide">{result.ticker}</span>
        </h2>
        <p className="text-[11px] text-paper/30 tabular-nums mt-0.5">
          {firstDate} — {lastDate}
        </p>
      </div>

      <MetricCards strategy={result.metrics} benchmark={result.benchmark_metrics} />

      <div className="bg-panel border border-line rounded p-5">
        <h3 className="text-[10px] uppercase tracking-widest text-paper/40 mb-4">Equity Curve vs Buy &amp; Hold</h3>
        <EquityChart strategyCurve={result.equity_curve} benchmarkCurve={result.benchmark_equity_curve} />
      </div>

      <div className="bg-panel border border-line rounded p-5">
        <h3 className="text-[10px] uppercase tracking-widest text-paper/40 mb-4">Price &amp; Trade Markers</h3>
        <PriceChart priceData={result.price_data} trades={result.trades} />
      </div>

      <div className="bg-panel border border-line rounded p-5">
        <h3 className="text-[10px] uppercase tracking-widest text-paper/40 mb-4">
          Trade Log <span className="text-paper/25">({result.trades.length})</span>
        </h3>
        <TradeLog trades={result.trades} />
      </div>
    </div>
  )
}
