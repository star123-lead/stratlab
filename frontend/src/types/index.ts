export interface ParamDefinition {
  key: string
  label: string
  default: number
  min: number
  max: number
}

export interface StrategyInfo {
  id: string
  name: string
  short_description: string
  how_it_works: string
  entry_rule: string
  exit_rule: string
  pros: string[]
  cons: string[]
  best_conditions: string
  default_params: Record<string, number>
  param_definitions: ParamDefinition[]
}

export interface Metrics {
  total_return_pct: number
  cagr_pct: number
  max_drawdown_pct: number
  sharpe_ratio: number
  win_rate_pct: number
  num_trades: number
  final_value: number
}

export interface EquityPoint {
  date: string
  value: number
}

export interface PricePoint {
  date: string
  close: number
  in_position: number
}

export interface Trade {
  entry_date: string
  exit_date: string
  entry_price: number
  exit_price: number
  shares: number
  pnl: number
  return_pct: number
}

export interface BacktestResult {
  ticker: string
  strategy_id: string
  strategy_name: string
  metrics: Metrics
  benchmark_metrics: Metrics
  equity_curve: EquityPoint[]
  benchmark_equity_curve: EquityPoint[]
  price_data: PricePoint[]
  trades: Trade[]
}

export interface BacktestRequest {
  ticker: string
  strategy_id: string
  params: Record<string, number>
  start_date: string
  end_date: string
  initial_capital: number
  commission_pct: number
}
