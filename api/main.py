from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "engine"))
from run_backtest import run_backtest
from strategy import SMAStrategy, DonchianChannelStrategy, BollingerBandsRSIStrategy


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class BacktestRequest(BaseModel):
    ticker: str
    start: str
    end: str
    initial_cash: float
    slippage: float
    commission: float
    strategy_type: str
    strategy_params: dict

@app.post("/backtest")
def run_backtest_endpoint(request: BacktestRequest):
    if request.strategy_type == "sma":
        strategy = SMAStrategy(short_window=request.strategy_params["short_window"], long_window=request.strategy_params["long_window"])

    elif request.strategy_type == "donchian":
        strategy = DonchianChannelStrategy(window=request.strategy_params["window"])

    elif request.strategy_type == "bollinger_bands_rsi":
        strategy = BollingerBandsRSIStrategy(
            window=request.strategy_params["window"],
            stdev=request.strategy_params["stdev"],
            rsi_window=request.strategy_params["rsi_window"],
            rsi_overbought=request.strategy_params["rsi_overbought"],
            rsi_oversold=request.strategy_params["rsi_oversold"]
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unknown strategy type: {request.strategy_type}")

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