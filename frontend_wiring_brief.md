# Brief for Claude Code — Wire Frontend to Real Backend

## Context

The backend is fully built, tested, and running locally via:
```
uvicorn api.main:app --reload
```
It's live at `http://127.0.0.1:8000` with CORS already configured to accept
requests from `http://localhost:5173` (the Vite dev server).

The frontend currently has a skeleton with dummy/placeholder data. Your
job now is to replace the dummy data with a real API call, and make
the strategy selection dynamic since the backend now supports three
different strategies with different parameters.

## The real, current API contract

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
  "strategy_type": "sma",
  "strategy_params": { "short_window": 50, "long_window": 100 }
}
```

`strategy_type` must be one of exactly three strings: `"sma"`,
`"donchian"`, or `"bollinger_bands_rsi"`. The `strategy_params` object's
shape depends entirely on which `strategy_type` is chosen:

- `"sma"` needs: `{ "short_window": int, "long_window": int }`
- `"donchian"` needs: `{ "window": int }`
- `"bollinger_bands_rsi"` needs: `{ "window": int, "stdev": float, "rsi_window": int, "rsi_overbought": float, "rsi_oversold": float }`

**Response body (JSON):**
```json
{
  "Total Return": -0.0209,
  "Max Drawdown": -0.1352,
  "Sharpe Ratio": -0.1180
}
```
Always exactly these three keys, always plain floats. `Total Return`
and `Max Drawdown` are decimals representing percentages (format as %
in the UI). Errors come back as a 400 status with a `detail` field
explaining what went wrong (e.g. invalid ticker, bad date range,
unknown strategy_type) — show this to the user rather than a generic
failure message.

## What to build

1. **Strategy selector** — a dropdown/select with three options: "SMA
   Crossover", "Donchian Breakout", "Bollinger Bands + RSI".

2. **Dynamic parameter fields** — the form fields shown underneath the
   strategy selector should change based on which strategy is picked,
   matching the `strategy_params` shape above exactly:
   - SMA selected → show Short Window, Long Window (defaults 50, 100)
   - Donchian selected → show Window (default 20)
   - Bollinger+RSI selected → show Window (default 20), Std Dev
     (default 2), RSI Window (default 14), RSI Overbought (default 70),
     RSI Oversold (default 30)

3. **Remove the old hardcoded short_window/long_window fields** if they
   exist as fixed fields outside this dynamic system — they should now
   only appear when SMA is the selected strategy.

4. **Wire the "Run Backtest" button** to actually POST to
   `http://127.0.0.1:8000/backtest`, building the request body from the
   current form state (ticker, dates, initial cash, slippage, commission,
   plus the strategy_type and the currently-relevant strategy_params).

5. **Loading state** while the request is in flight (this can take
   several seconds due to fetching real market data).

6. **Error handling** — if the response is not OK, show the `detail`
   message from the response body to the user, clearly, rather than
   failing silently or showing a generic error.

7. **Results display** — replace dummy metric values with the real
   response: Total Return and Max Drawdown as percentages (colour-coded
   green/red for positive/negative is a nice touch), Sharpe Ratio as a
   plain number.

## Explicitly still out of scope

- No chart yet — that's a separate task, coming next, and needs a
  backend change first (returning a time series, not just final
  numbers) — don't build a chart against fake data now.
- No trade history table — the backend doesn't track individual trades.
- No file upload feature.
- No deployment/production config — this should all point at
  `http://127.0.0.1:8000` for now; a public backend URL will replace
  this later, but don't build environment-variable switching for it
  yet unless it's trivial to add.

## Notes

- If you hit a CORS error, the backend's `allow_origins` is currently
  locked to exactly `http://localhost:5173` — if the dev server is
  running on a different port, flag it rather than silently changing
  `api/main.py`.
- Keep the implementation straightforward — this is a CV/portfolio
  piece, clarity matters more than architectural sophistication.
