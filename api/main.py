from fastapi import FastAPI
from pydantic import BaseModel
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "engine"))
from run_backtest import run_backtest
from strategy import SMAStrategy


app = FastAPI()

class BacktestRequest(BaseModel):
    ticker: str
    start: str
    end: str
    initial_cash: float
    slippage: float
    commission: float
    short_window: int
    long_window: int

@app.post("/backtest")
def run_backtest_endpoint(request: BacktestRequest):
    strategy = SMAStrategy(short_window=request.short_window, long_window=request.long_window)
    results = run_backtest(
        ticker=request.ticker,
        start=request.start,
        end=request.end,
        strategy=strategy,
        initial_cash=request.initial_cash,
        slippage=request.slippage,
        commission=request.commission
    )
    return results