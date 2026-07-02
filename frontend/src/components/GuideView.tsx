import type { StrategyInfo } from '../types'

export default function GuideView({ strategies }: { strategies: StrategyInfo[] }) {
  if (strategies.length === 0) {
    return <p className="text-sm text-paper/40">Loading strategy guide…</p>
  }

  return (
    <div className="space-y-5">
      {strategies.map((s) => (
        <div key={s.id} className="bg-panel border border-line rounded p-6">
          <h3 className="font-display text-lg font-semibold text-amber mb-1">{s.name}</h3>
          <p className="text-sm text-paper/50 mb-4">{s.short_description}</p>

          <p className="text-sm text-paper/80 leading-relaxed mb-4">{s.how_it_works}</p>

          <div className="grid sm:grid-cols-2 gap-3 mb-5">
            <div className="bg-ink rounded p-3 border border-line">
              <div className="text-[10px] uppercase tracking-widest text-up mb-1">Entry Rule</div>
              <div className="text-sm text-paper/80">{s.entry_rule}</div>
            </div>
            <div className="bg-ink rounded p-3 border border-line">
              <div className="text-[10px] uppercase tracking-widest text-down mb-1">Exit Rule</div>
              <div className="text-sm text-paper/80">{s.exit_rule}</div>
            </div>
          </div>

          {(s.pros.length > 0 || s.cons.length > 0) && (
            <div className="grid sm:grid-cols-2 gap-5 mb-5">
              <div>
                <div className="text-[10px] uppercase tracking-widest text-paper/40 mb-1.5">Pros</div>
                <ul className="space-y-1">
                  {s.pros.map((p, i) => (
                    <li key={i} className="text-sm text-paper/70 flex gap-2">
                      <span className="text-up">+</span> {p}
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <div className="text-[10px] uppercase tracking-widest text-paper/40 mb-1.5">Cons</div>
                <ul className="space-y-1">
                  {s.cons.map((c, i) => (
                    <li key={i} className="text-sm text-paper/70 flex gap-2">
                      <span className="text-down">–</span> {c}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          <div className="text-xs text-paper/40 border-t border-line pt-3">
            <span className="text-paper/60">Best in:</span> {s.best_conditions}
          </div>
        </div>
      ))}
    </div>
  )
}
