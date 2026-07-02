import type { BacktestRequest, BacktestResult, StrategyInfo } from '../types'

const BASE =import.meta.env.VITE_API_URL || '/api'

export async function getStrategies(): Promise<StrategyInfo[]> {
  const res = await fetch(`${BASE}/strategies`)
  if (!res.ok) throw new Error('Could not load strategies from the backend.')
  return res.json()
}

export async function runBacktest(req: BacktestRequest): Promise<BacktestResult> {
  const res = await fetch(`${BASE}/backtest`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Backtest failed.' }))
    throw new Error(err.detail || 'Backtest failed.')
  }
  return res.json()
}
