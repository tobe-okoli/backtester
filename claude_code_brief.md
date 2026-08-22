# Brief for Claude Code — Backtester Frontend

## Context

This is a portfolio project: a Python backtesting engine (pandas-based),
wrapped in a FastAPI backend, with a React (Vite) frontend that's been
scaffolded but not yet built out. The backend is fully working, tested,
and running locally. Your job is the frontend only.

## What already exists — do not modify

- `engine/` — the backtesting logic (data fetching, strategy, execution,
  portfolio simulation, metrics). Fully built and tested. Don't touch.
- `api/main.py` — a working FastAPI server exposing one endpoint. Don't
  touch unless I explicitly ask you to change the API contract.
- `tests/` — pytest tests covering the engine. Don't touch.
- `frontend/` — a fresh Vite + React scaffold (JavaScript, not
  TypeScript), using ESLint. This is what you'll be building out.

## The API contract (this is real and working — build against it exactly)

**Endpoint:** `POST http://127.0.0.1:8000/backtest`

**Request body (JSON):**
```json
{
  "ticker": "AAPL",
  "start": "2023-01-01",
  "end": "2024-01-01",
  "initial_cash": 10000,
  "slippage": 0.001,
  "commission": 0.001,
  "short_window": 50,
  "long_window": 100
}
```

**Response body (JSON):**
```json
{
  "Total Return": -0.0209,
  "Max Drawdown": -0.1352,
  "Sharpe Ratio": -0.1180
}
```

All three response values are plain floats. `Total Return` and
`Max Drawdown` are decimals representing percentages (e.g. -0.0209 means
-2.09%) — format them as percentages in the UI rather than raw decimals.

Only one strategy currently exists on the backend — a simple moving
average crossover, configured via `short_window` and `long_window`. Don't
build UI for other strategies yet; there's nowhere for that to go on the
backend.

## What to build (v1 scope)

1. A form with fields matching the request body above: ticker (text
   input), start date, end date, initial cash, slippage, commission,
   short window, long window. Sensible defaults are fine (e.g. AAPL,
   2023-01-01 to 2024-01-01, 10000, 0.001, 0.001, 50, 100).
2. A "Run Backtest" button that POSTs the form data to the endpoint above.
3. A results panel showing the three returned metrics clearly, once the
   request completes. Total Return and Max Drawdown as percentages,
   colour-coded (green for positive, red for negative) is a nice touch
   but not required.
4. Basic loading state while the request is in flight (the backend call
   can take several seconds due to fetching real market data), and basic
   error handling if the request fails (e.g. invalid ticker, bad date
   range — the backend returns clear error messages for these).
5. Reasonably clean, modern styling. Doesn't need to be elaborate.

## Explicitly out of scope for v1 — do not build these

- No file upload / arbitrary strategy upload feature
- No trade history table (the backend doesn't track individual trades
  yet, only aggregate metrics)
- No equity curve chart (the backend doesn't return a time series yet,
  only final metrics) — this may be added in a future backend update
- No strategy selector dropdown (only one strategy exists server-side)
- No authentication, no persistence/database, no multi-user support

## Notes

- CORS: the FastAPI backend may need CORS middleware added to accept
  requests from `http://localhost:5173` (the Vite dev server's default
  port). Flag this if you hit a CORS error — I'd rather review that
  change than have it silently added, since it's a change to `api/main.py`.
- Keep the implementation straightforward. This is a CV/portfolio piece,
  not a production app — clarity and a working demo matter more than
  architectural sophistication.
