from data import fetch_stock_data
from execution import Execution
from portfolio import Portfolio
import metrics
from strategy import Strategy

def run_backtest(ticker : str, start : str, end :str , strategy : Strategy, initial_cash: float) -> dict:

  data = fetch_stock_data(ticker, start, end)
  signals = strategy.generate_signals(data)
  execution = Execution(0.001, 0.001)

  port = Portfolio(data, signals, initial_cash, execution)
  final_port = port.simulate_trades()

  total_return = metrics.calculate_total_return(final_port)
  max_drawdown = metrics.calculate_max_drawdown(final_port)
  sr = metrics.calculate_sharpe(final_port)

  results = {"Total Return": total_return, "Max Drawdown": max_drawdown, "Sharpe Ratio": sr}
  

  return results


if __name__ == "__main__":
  from strategy import SMAStrategy
  result = run_backtest("AAPL", "2023-01-01","2024-01-01", SMAStrategy(short_window=50, long_window=100),10000 )
  print(result)


