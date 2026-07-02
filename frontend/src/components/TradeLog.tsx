import type { Trade } from '../types'

export default function TradeLog({ trades }: { trades: Trade[] }) {
  if (trades.length === 0) {
    return (
      <p className="text-sm text-paper/40">
        No trades triggered in this range — try a longer date range or different parameters.
      </p>
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-xs">
        <thead>
          <tr className="text-left text-paper/40 border-b border-line uppercase tracking-widest text-[10px]">
            <th className="py-2 pr-4 font-medium">#</th>
            <th className="py-2 pr-4 font-medium">Entry</th>
            <th className="py-2 pr-4 font-medium">Exit</th>
            <th className="py-2 pr-4 font-medium">Entry Px</th>
            <th className="py-2 pr-4 font-medium">Exit Px</th>
            <th className="py-2 pr-4 font-medium">P&amp;L</th>
            <th className="py-2 pr-4 font-medium">Return</th>
          </tr>
        </thead>
        <tbody>
          {trades.map((t, i) => (
            <tr key={i} className="border-b border-line/50">
              <td className="py-2 pr-4 text-paper/30">{i + 1}</td>
              <td className="py-2 pr-4 text-paper/70">{t.entry_date}</td>
              <td className="py-2 pr-4 text-paper/70">{t.exit_date}</td>
              <td className="py-2 pr-4 text-paper/50 tabular-nums">${t.entry_price.toFixed(2)}</td>
              <td className="py-2 pr-4 text-paper/50 tabular-nums">${t.exit_price.toFixed(2)}</td>
              <td className={`py-2 pr-4 font-medium tabular-nums ${t.pnl >= 0 ? 'text-up' : 'text-down'}`}>
                {t.pnl >= 0 ? '+' : ''}
                {t.pnl.toFixed(2)}
              </td>
              <td className={`py-2 pr-4 font-medium tabular-nums ${t.return_pct >= 0 ? 'text-up' : 'text-down'}`}>
                {t.return_pct >= 0 ? '+' : ''}
                {t.return_pct.toFixed(2)}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
