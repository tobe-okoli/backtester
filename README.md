# Algorithmic Backtesting Engine

A modular Python backtesting engine for evaluating quantitative trading strategies against historical OHLCV data, with a FastAPI backend and React frontend for configuring runs and visualising performance.

## Performance

The portfolio simulation was benchmarked using synthetic OHLCV datasets ranging from 10,000 to 1,000,000 bars.

|      Bars | `iterrows()` | `itertuples()` |   NumPy | Final speedup |
| --------: | -----------: | -------------: | ------: | ------------: |
|    10,000 |      0.154 s |        0.037 s | 0.006 s |         24.8× |
|   100,000 |      1.522 s |        0.372 s | 0.062 s |         24.6× |
| 1,000,000 |     16.096 s |        4.614 s | 0.616 s |         26.1× |

On the 1,000,000-bar benchmark, processing performance increased from approximately **62,000 bars/s to 1.62 million bars/s**.

The original portfolio loop used pandas `iterrows()`. Replacing it with `itertuples()` reduced row-iteration overhead and improved the 1M-bar benchmark by roughly **3.5×**. The loop was then changed to use NumPy arrays directly, producing a final ~26× speedup while keeping the same trading and portfolio behaviour.

## Architecture

```text
                ┌─────────────┐
                │   data.py   │  Loads & prepares historical OHLCV data
                └──────┬──────┘
                       ▼
                ┌─────────────┐
                │ strategy.py │  Pluggable strategy interface (SMA, Donchian, BB+RSI)
                └──────┬──────┘
                       ▼
                ┌─────────────┐
                │execution.py │  Simulates fills with slippage & commission
                └──────┬──────┘
                       ▼
                ┌─────────────┐
                │portfolio.py │  Tracks cash, positions and portfolio value
                └──────┬──────┘
                       ▼
                ┌─────────────┐
                │ metrics.py  │  Sharpe ratio, max drawdown, total return
                └──────┬──────┘
                       ▼
                ┌───────────────┐
                │run_backtest.py│  Orchestrates the full pipeline
                └──────┬────────┘
                       ▼
              FastAPI REST endpoint ──▶ React frontend
```

## Strategies

The engine currently supports:

* Simple Moving Average crossover
* Donchian Channel breakout
* Bollinger Bands + RSI

Each strategy implements a common strategy interface and generates trading signals from historical price data.

## Features

* Modular strategy architecture for adding and testing different trading strategies
* Historical OHLCV data retrieval
* Configurable initial cash, slippage and commission
* Portfolio simulation with cash, position and portfolio value tracking
* Performance metrics including total return, Sharpe ratio and maximum drawdown
* FastAPI backend for submitting configurable backtests
* React frontend for configuring runs and viewing results
* Automated testing with pytest and GitHub Actions

## Tech Stack

**Backend:** Python, FastAPI, NumPy, pandas, yfinance
**Frontend:** React, Vite
**Testing & CI:** pytest, pytest-cov, GitHub Actions

## Testing

The engine is tested with `pytest`, covering strategy behaviour, execution logic, portfolio simulation, performance metrics and portfolio edge cases. Current engine test coverage is approximately **80%**.

GitHub Actions automatically runs the test suite on pushes and pull requests.

Run the tests locally with:

```bash
pytest tests/ -v --cov=engine --cov-report=term-missing
```
