import { useState } from 'react'
import './App.css'

const API_URL = 'http://127.0.0.1:8000/backtest'

const STRATEGY_OPTIONS = [
  { value: 'sma', label: 'SMA Crossover' },
  { value: 'donchian', label: 'Donchian Breakout' },
  { value: 'bollinger_bands_rsi', label: 'Bollinger Bands + RSI' },
]

// Field definitions per strategy — key must match the backend's
// strategy_params shape exactly.
const STRATEGY_FIELDS = {
  sma: [
    { key: 'short_window', label: 'Short Window', default: 50 },
    { key: 'long_window', label: 'Long Window', default: 100 },
  ],
  donchian: [{ key: 'window', label: 'Window', default: 20 }],
  bollinger_bands_rsi: [
    { key: 'window', label: 'Window', default: 20 },
    { key: 'stdev', label: 'Std Dev', default: 2, step: '0.1' },
    { key: 'rsi_window', label: 'RSI Window', default: 14 },
    { key: 'rsi_overbought', label: 'RSI Overbought', default: 70 },
    { key: 'rsi_oversold', label: 'RSI Oversold', default: 30 },
  ],
}

function defaultParamsFor(strategyType) {
  const params = {}
  for (const field of STRATEGY_FIELDS[strategyType]) {
    params[field.key] = field.default
  }
  return params
}

function formatPercent(value) {
  return `${(value * 100).toFixed(2)}%`
}

function MetricCard({ label, value, isPercent }) {
  const isNegative = value < 0
  return (
    <div className="metric-card">
      <div className="metric-label">{label}</div>
      <div className={`metric-value ${isNegative ? 'negative' : 'positive'}`}>
        {isPercent ? formatPercent(value) : value.toFixed(2)}
      </div>
    </div>
  )
}

// FastAPI validation errors can return `detail` as a string or as a list
// of pydantic error objects — normalize either into a readable string.
function extractErrorMessage(body) {
  if (!body) return 'Something went wrong.'
  const { detail } = body
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail
      .map((err) => err.msg || JSON.stringify(err))
      .join('; ')
  }
  return 'Something went wrong.'
}

function App() {
  const [form, setForm] = useState({
    ticker: 'AAPL',
    start: '2023-01-01',
    end: '2024-01-01',
    initialCash: 10000,
    slippage: 0.001,
    commission: 0.001,
  })
  const [strategyType, setStrategyType] = useState('sma')
  const [strategyParams, setStrategyParams] = useState(defaultParamsFor('sma'))
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [results, setResults] = useState(null)

  const handleChange = (field) => (e) => {
    setForm((prev) => ({ ...prev, [field]: e.target.value }))
  }

  const handleStrategyChange = (e) => {
    const nextType = e.target.value
    setStrategyType(nextType)
    setStrategyParams(defaultParamsFor(nextType))
  }

  const handleParamChange = (key) => (e) => {
    setStrategyParams((prev) => ({ ...prev, [key]: e.target.value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResults(null)

    const numericParams = Object.fromEntries(
      Object.entries(strategyParams).map(([key, value]) => [key, Number(value)]),
    )

    const body = {
      ticker: form.ticker,
      start: form.start,
      end: form.end,
      initial_cash: Number(form.initialCash),
      slippage: Number(form.slippage),
      commission: Number(form.commission),
      strategy_type: strategyType,
      strategy_params: numericParams,
    }

    let response
    try {
      response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
    } catch {
      setError('Could not reach the backend. Is it running on http://127.0.0.1:8000?')
      setLoading(false)
      return
    }

    // The backend is expected to return JSON, but errors can arrive as a
    // plain-text body (e.g. an uncaught server exception) — don't let a
    // parse failure masquerade as "backend unreachable".
    let data = null
    try {
      data = await response.json()
    } catch {
      // leave data as null; handled below
    }

    if (!response.ok) {
      setError(
        data ? extractErrorMessage(data) : `Request failed: ${response.status} ${response.statusText}`,
      )
    } else {
      setResults(data)
    }
    setLoading(false)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Backtester</h1>
      </header>

      <main className="app-main">
        <form className="backtest-form" onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="ticker">Ticker</label>
            <input
              id="ticker"
              type="text"
              value={form.ticker}
              onChange={handleChange('ticker')}
            />
          </div>

          <div className="field">
            <label htmlFor="start">Start Date</label>
            <input
              id="start"
              type="date"
              value={form.start}
              onChange={handleChange('start')}
            />
          </div>

          <div className="field">
            <label htmlFor="end">End Date</label>
            <input
              id="end"
              type="date"
              value={form.end}
              onChange={handleChange('end')}
            />
          </div>

          <div className="field">
            <label htmlFor="initialCash">Initial Cash</label>
            <input
              id="initialCash"
              type="number"
              value={form.initialCash}
              onChange={handleChange('initialCash')}
            />
          </div>

          <div className="field">
            <label htmlFor="slippage">Slippage</label>
            <input
              id="slippage"
              type="number"
              step="0.001"
              value={form.slippage}
              onChange={handleChange('slippage')}
            />
          </div>

          <div className="field">
            <label htmlFor="commission">Commission</label>
            <input
              id="commission"
              type="number"
              step="0.001"
              value={form.commission}
              onChange={handleChange('commission')}
            />
          </div>

          <div className="field strategy-field">
            <label htmlFor="strategyType">Strategy</label>
            <select
              id="strategyType"
              value={strategyType}
              onChange={handleStrategyChange}
            >
              {STRATEGY_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {STRATEGY_FIELDS[strategyType].map((paramField) => (
            <div className="field" key={paramField.key}>
              <label htmlFor={paramField.key}>{paramField.label}</label>
              <input
                id={paramField.key}
                type="number"
                step={paramField.step}
                value={strategyParams[paramField.key]}
                onChange={handleParamChange(paramField.key)}
              />
            </div>
          ))}

          <button type="submit" className="run-button" disabled={loading}>
            {loading ? 'Running…' : 'Run Backtest'}
          </button>
        </form>

        {error && <div className="error-banner">{error}</div>}

        {results && (
          <section className="results">
            <h2>Results</h2>
            <div className="metrics-row">
              <MetricCard
                label="Total Return"
                value={results['Total Return']}
                isPercent
              />
              <MetricCard
                label="Max Drawdown"
                value={results['Max Drawdown']}
                isPercent
              />
              <MetricCard label="Sharpe Ratio" value={results['Sharpe Ratio']} />
            </div>
          </section>
        )}
      </main>
    </div>
  )
}

export default App
