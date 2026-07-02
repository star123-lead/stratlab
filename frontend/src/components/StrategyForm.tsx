import { useEffect, useState } from 'react'
import type { StrategyInfo } from '../types'

interface Props {
  strategies: StrategyInfo[]
  onRun: (req: {
    ticker: string
    strategy_id: string
    params: Record<string, number>
    start_date: string
    end_date: string
    initial_capital: number
    commission_pct: number
  }) => void
  loading: boolean
}

function defaultStartDate() {
  const d = new Date()
  d.setFullYear(d.getFullYear() - 2)
  return d.toISOString().slice(0, 10)
}

function defaultEndDate() {
  return new Date().toISOString().slice(0, 10)
}

const fieldClass =
  'w-full bg-ink border border-line rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-amber'
const labelClass = 'block text-[10px] uppercase tracking-widest text-paper/40 mb-1.5'

export default function StrategyForm({ strategies, onRun, loading }: Props) {
  const [ticker, setTicker] = useState('AAPL')
  const [strategyId, setStrategyId] = useState('')
  const [params, setParams] = useState<Record<string, number>>({})
  const [startDate, setStartDate] = useState(defaultStartDate())
  const [endDate, setEndDate] = useState(defaultEndDate())
  const [capital, setCapital] = useState(10000)
  const [commission, setCommission] = useState(0.1)

  useEffect(() => {
    if (strategies.length && !strategyId) setStrategyId(strategies[0].id)
  }, [strategies, strategyId])

  useEffect(() => {
    const strat = strategies.find((s) => s.id === strategyId)
    if (strat) setParams(strat.default_params)
  }, [strategyId, strategies])

  const strat = strategies.find((s) => s.id === strategyId)

  function submit(e: React.FormEvent) {
    e.preventDefault()
    onRun({
      ticker: ticker.trim().toUpperCase(),
      strategy_id: strategyId,
      params,
      start_date: startDate,
      end_date: endDate,
      initial_capital: capital,
      commission_pct: commission,
    })
  }

  return (
    <form onSubmit={submit} className="bg-panel border border-line rounded p-5 space-y-4 h-fit">
      <div>
        <label className={labelClass}>Ticker Symbol</label>
        <input
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          placeholder="AAPL, MSFT, RELIANCE.NS"
          className={`${fieldClass} uppercase tracking-wide`}
        />
      </div>

      <div>
        <label className={labelClass}>Strategy</label>
        <select value={strategyId} onChange={(e) => setStrategyId(e.target.value)} className={fieldClass}>
          {strategies.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>
      </div>

      {strat && strat.param_definitions.length > 0 && (
        <div className="grid grid-cols-2 gap-3">
          {strat.param_definitions.map((p) => (
            <div key={p.key}>
              <label className={labelClass}>{p.label}</label>
              <input
                type="number"
                min={p.min}
                max={p.max}
                value={params[p.key] ?? p.default}
                onChange={(e) => setParams({ ...params, [p.key]: Number(e.target.value) })}
                className={fieldClass}
              />
            </div>
          ))}
        </div>
      )}

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className={labelClass}>Start Date</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className={fieldClass}
          />
        </div>
        <div>
          <label className={labelClass}>End Date</label>
          <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} className={fieldClass} />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className={labelClass}>Initial Capital</label>
          <input
            type="number"
            min={100}
            value={capital}
            onChange={(e) => setCapital(Number(e.target.value))}
            className={fieldClass}
          />
        </div>
        <div>
          <label className={labelClass}>Commission %</label>
          <input
            type="number"
            min={0}
            step={0.05}
            value={commission}
            onChange={(e) => setCommission(Number(e.target.value))}
            className={fieldClass}
          />
        </div>
      </div>

      {strat && (
        <p className="text-xs text-paper/40 leading-relaxed border-t border-line pt-3">{strat.short_description}</p>
      )}

      <button
        type="submit"
        disabled={loading || !strategyId}
        className="w-full bg-amber hover:bg-amber-dim disabled:opacity-40 disabled:cursor-not-allowed text-ink font-display font-semibold rounded py-2.5 text-xs uppercase tracking-widest transition focus:outline-none focus-visible:ring-2 focus-visible:ring-amber"
      >
        {loading ? 'Running…' : 'Run Backtest'}
      </button>
    </form>
  )
}
