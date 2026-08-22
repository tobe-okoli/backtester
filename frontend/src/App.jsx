import { useState } from 'react'
import './App.css'

// Dummy results — visual placeholder only, not wired to the backend yet.
const DUMMY_RESULTS = {
  totalReturn: -0.0210,
  maxDrawdown: -0.1352,
  sharpeRatio: -0.12,
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

function App() {
  const [form, setForm] = useState({
    ticker: 'AAPL',
    start: '2023-01-01',
    end: '2024-01-01',
    initialCash: 10000,
    slippage: 0.001,
    commission: 0.001,
    shortWindow: 50,
    longWindow: 100,
  })

  const handleChange = (field) => (e) => {
    setForm((prev) => ({ ...prev, [field]: e.target.value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    // Visual pass only — no API call wired up yet.
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

          <div className="field">
            <label htmlFor="shortWindow">Short Window</label>
            <input
              id="shortWindow"
              type="number"
              value={form.shortWindow}
              onChange={handleChange('shortWindow')}
            />
          </div>

          <div className="field">
            <label htmlFor="longWindow">Long Window</label>
            <input
              id="longWindow"
              type="number"
              value={form.longWindow}
              onChange={handleChange('longWindow')}
            />
          </div>

          <button type="submit" className="run-button">
            Run Backtest
          </button>
        </form>

        <section className="results">
          <h2>Results</h2>
          <div className="metrics-row">
            <MetricCard
              label="Total Return"
              value={DUMMY_RESULTS.totalReturn}
              isPercent
            />
            <MetricCard
              label="Max Drawdown"
              value={DUMMY_RESULTS.maxDrawdown}
              isPercent
            />
            <MetricCard label="Sharpe Ratio" value={DUMMY_RESULTS.sharpeRatio} />
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
