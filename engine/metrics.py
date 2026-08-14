import pandas as pd
from data import fetch_stock_data
from strategy import SMAStrategy
from portfolio import Portfolio

def calculate_total_return (portolfio_data : pd.DataFrame) -> float:
  initial_value = portolfio_data.iat[0, 0]
  final_value = portolfio_data.iat[-1,0]

  total_return = (final_value - initial_value) / initial_value

  return total_return

def calculate_max_drawdown(portfolio_data : pd.DataFrame) -> float:
  portfolio_data['Running Peak'] = portfolio_data['Total Value'].cummax()




if __name__ == "__main__":

  #DEBUGGING

  data = pd.read_csv("AAPL_data.csv", index_col="Date", parse_dates=True)
  strategy = SMAStrategy(short_window=50, long_window=100)
  signals = strategy.generate_signals(data)

  portfolio_test = Portfolio(data, signals, 10000 )
  portfolio_output = portfolio_test.simulate_trades()

  result = calculate_max_drawdown(portfolio_output)
  print(result)

