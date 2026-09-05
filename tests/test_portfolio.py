import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "engine"))

from execution import Execution
from portfolio import Portfolio

def test_portfolio_simulation():
    data = pd.DataFrame({"Close": [100.0, 110.0, 120.0]}, index=pd.date_range("2023-01-01", periods=3))
    signals = pd.Series([1, 0, -1], index=data.index)
    execution = Execution(slippage=0.0, commission=0.0)

    portfolio = Portfolio(data, signals, initial_cash=1000, execution=execution)
    result = portfolio.simulate_trades()

    expected = pd.DataFrame({"Total Value": [1000.0, 1100.0, 1200.0]}, index=data.index)
    pd.testing.assert_frame_equal(result, expected)