import { useEffect, useState } from 'react'
import { getStrategies } from './lib/api'
import type { StrategyInfo } from './types'
import BacktestView from './components/BacktestView'
import GuideView from './components/GuideView'

type Tab = 'backtest' | 'guide'

export default function App() {
  const [tab, setTab] = useState<Tab>('backtest')
  const [strategies, setStrategies] = useState<StrategyInfo[]>([])
  const [loadError, setLoadError] = useState<string | null>(null)

  useEffect(() => {
    getStrategies()
      .then(setStrategies)
      .catch(() =>
        setLoadError(
          "Can't reach the backend. Start it with `uvicorn main:app --reload` from the backend/ folder, then reload this page.",
        ),
      )
  }, [])

  return (
    <div className="min-h-screen bg-ink text-paper">
      <header className="border-b border-line px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <span className="relative flex h-2 w-2">
            <span className="motion-reduce:animate-none animate-ping absolute inline-flex h-full w-full rounded-full bg-amber opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-amber" />
          </span>
          <h1 className="font-display font-semibold text-lg tracking-tight">
            Strat<span className="text-amber">Lab</span>
          </h1>
        </div>

        <nav className="flex gap-1 bg-panel border border-line rounded p-1">
          <button
            onClick={() => setTab('backtest')}
            className={`px-4 py-1.5 rounded text-xs font-medium uppercase tracking-wide transition focus:outline-none focus-visible:ring-1 focus-visible:ring-amber ${
              tab === 'backtest' ? 'bg-amber text-ink' : 'text-paper/50 hover:text-paper'
            }`}
          >
            Backtest
          </button>
          <button
            onClick={() => setTab('guide')}
            className={`px-4 py-1.5 rounded text-xs font-medium uppercase tracking-wide transition focus:outline-none focus-visible:ring-1 focus-visible:ring-amber ${
              tab === 'guide' ? 'bg-amber text-ink' : 'text-paper/50 hover:text-paper'
            }`}
          >
            Guide
          </button>
        </nav>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {loadError && (
          <div className="mb-6 rounded border border-down/30 bg-down/10 px-4 py-3 text-sm text-down">
            {loadError}
          </div>
        )}
        {tab === 'backtest' && <BacktestView strategies={strategies} />}
        {tab === 'guide' && <GuideView strategies={strategies} />}
      </main>
    </div>
  )
}
