import { useState } from 'react'
import { runBacktest } from '../lib/api'
import type { BacktestRequest, BacktestResult, StrategyInfo } from '../types'
import StrategyForm from './StrategyForm'
import ResultsPanel from './ResultsPanel'

export default function BacktestView({ strategies }: { strategies: StrategyInfo[] }) {
  const [result, setResult] = useState<BacktestResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleRun(req: BacktestRequest) {
    setLoading(true)
    setError(null)
    try {
      const res = await runBacktest(req)
      setResult(res)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Something went wrong.')
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[340px_1fr] gap-6">
      <StrategyForm strategies={strategies} onRun={handleRun} loading={loading} />

      <div>
        {error && (
          <div className="rounded border border-down/30 bg-down/10 px-4 py-3 text-sm text-down mb-4">{error}</div>
        )}
        {!result && !error && (
          <div className="h-full min-h-[24rem] flex items-center justify-center rounded border border-dashed border-line text-paper/30 text-xs uppercase tracking-widest">
            Pick a ticker and strategy, then run a backtest
          </div>
        )}
        {result && <ResultsPanel result={result} />}
      </div>
    </div>
  )
}
