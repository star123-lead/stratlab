import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import type { EquityPoint } from '../types'

export default function EquityChart({
  strategyCurve,
  benchmarkCurve,
}: {
  strategyCurve: EquityPoint[]
  benchmarkCurve: EquityPoint[]
}) {
  const data = strategyCurve.map((p, i) => ({
    date: p.date,
    strategy: p.value,
    benchmark: benchmarkCurve[i]?.value ?? null,
  }))

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#2A2D33" />
        <XAxis dataKey="date" tick={{ fontSize: 10, fill: '#E8E6E1', opacity: 0.4 }} minTickGap={50} />
        <YAxis tick={{ fontSize: 10, fill: '#E8E6E1', opacity: 0.4 }} width={64} />
        <Tooltip
          contentStyle={{ background: '#16181C', border: '1px solid #2A2D33', borderRadius: 4, fontSize: 12 }}
          labelStyle={{ color: '#E8E6E1' }}
        />
        <Legend wrapperStyle={{ fontSize: 11, textTransform: 'uppercase', letterSpacing: '0.05em' }} />
        <Line type="monotone" dataKey="strategy" name="Strategy" stroke="#FF9F1C" dot={false} strokeWidth={2} />
        <Line
          type="monotone"
          dataKey="benchmark"
          name="Buy & Hold"
          stroke="#E8E6E1"
          strokeOpacity={0.35}
          dot={false}
          strokeWidth={1.5}
          strokeDasharray="4 3"
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
