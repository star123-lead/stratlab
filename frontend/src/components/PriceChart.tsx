import { Area, AreaChart, CartesianGrid, ReferenceDot, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import type { PricePoint, Trade } from '../types'

export default function PriceChart({ priceData, trades }: { priceData: PricePoint[]; trades: Trade[] }) {
  const priceByDate = new Map(priceData.map((p) => [p.date, p.close]))

  return (
    <ResponsiveContainer width="100%" height={260}>
      <AreaChart data={priceData}>
        <defs>
          <linearGradient id="priceFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#FF9F1C" stopOpacity={0.25} />
            <stop offset="95%" stopColor="#FF9F1C" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#2A2D33" />
        <XAxis dataKey="date" tick={{ fontSize: 10, fill: '#E8E6E1', opacity: 0.4 }} minTickGap={50} />
        <YAxis tick={{ fontSize: 10, fill: '#E8E6E1', opacity: 0.4 }} width={56} domain={['auto', 'auto']} />
        <Tooltip
          contentStyle={{ background: '#16181C', border: '1px solid #2A2D33', borderRadius: 4, fontSize: 12 }}
          labelStyle={{ color: '#E8E6E1' }}
        />
        <Area type="monotone" dataKey="close" stroke="#FF9F1C" fill="url(#priceFill)" strokeWidth={1.5} />
        {trades.map((t, i) => (
          <ReferenceDot
            key={`buy-${i}`}
            x={t.entry_date}
            y={priceByDate.get(t.entry_date) ?? t.entry_price}
            r={4}
            fill="#3DDC84"
            stroke="#0A0B0D"
          />
        ))}
        {trades.map((t, i) => (
          <ReferenceDot
            key={`sell-${i}`}
            x={t.exit_date}
            y={priceByDate.get(t.exit_date) ?? t.exit_price}
            r={4}
            fill="#FF5C5C"
            stroke="#0A0B0D"
          />
        ))}
      </AreaChart>
    </ResponsiveContainer>
  )
}
