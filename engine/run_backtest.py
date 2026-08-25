from data import fetch_stock_data
from execution import Execution
from portfolio import Portfolio
import metrics
from strategy import Strategy

def run_backtest(ticker : str, start : str, end :str , strategy : Strategy, initial_cash: float, slippage : float, commission: float) -> dict:

  data = fetch_stock_data(ticker, start, end)
  signals = strategy.generate_signals(data)
  execution = Execution(slippage, commission)

  port = Portfolio(data, signals, initial_cash, execution)
  final_port = port.simulate_trades()

  total_return = metrics.calculate_total_return(final_port)
  max_drawdown = metrics.calculate_max_drawdown(final_port)
  sr = metrics.calculate_sharpe(final_port)

  results = {"Total Return": float(total_return), "Max Drawdown": float(max_drawdown), "Sharpe Ratio": float(sr)}
  

  return results



