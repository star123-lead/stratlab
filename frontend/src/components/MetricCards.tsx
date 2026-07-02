import type { Metrics } from '../types'
import { useCountUp } from '../lib/useCountUp'

type Tone = 'up' | 'down' | 'neutral'

function Card({
  label,
  value,
  format,
  sub,
  tone = 'neutral',
}: {
  label: string
  value: number
  format: (n: number) => string
  sub?: string
  tone?: Tone
}) {
  const animated = useCountUp(value)
  const colorClass = tone === 'up' ? 'text-up' : tone === 'down' ? 'text-down' : 'text-paper'

  return (
    <div className="bg-panel border border-line rounded p-4">
      <div className="text-[10px] uppercase tracking-widest text-paper/40 mb-1.5">{label}</div>
      <div className={`text-xl font-medium tabular-nums ${colorClass}`}>{format(animated)}</div>
      {sub && <div className="text-[10px] text-paper/30 mt-1 tabular-nums">{sub}</div>}
    </div>
  )
}

export default function MetricCards({ strategy, benchmark }: { strategy: Metrics; benchmark: Metrics }) {
  const pct = (n: number) => `${n >= 0 ? '+' : ''}${n.toFixed(2)}%`

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
      <Card
        label="Total Return"
        value={strategy.total_return_pct}
        format={pct}
        tone={strategy.total_return_pct >= 0 ? 'up' : 'down'}
        sub={`B&H ${pct(benchmark.total_return_pct)}`}
      />
      <Card
        label="CAGR"
        value={strategy.cagr_pct}
        format={pct}
        tone={strategy.cagr_pct >= 0 ? 'up' : 'down'}
      />
      <Card label="Max Drawdown" value={strategy.max_drawdown_pct} format={(n) => `${n.toFixed(2)}%`} tone="down" />
      <Card
        label="Sharpe Ratio"
        value={strategy.sharpe_ratio}
        format={(n) => n.toFixed(2)}
        tone={strategy.sharpe_ratio >= 0 ? 'up' : 'down'}
      />
      <Card label="Win Rate" value={strategy.win_rate_pct} format={(n) => `${n.toFixed(1)}%`} />
      <Card label="Trades" value={strategy.num_trades} format={(n) => `${Math.round(n)}`} />
    </div>
  )
}
