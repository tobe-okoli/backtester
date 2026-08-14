import pandas as pd

def calculate_total_return (portolfio_data : pd.DataFrame) -> float:
  initial_value = portolfio_data.iat[0, 0]
  final_value = portolfio_data.iat[-1,0]

  total_return = (final_value - initial_value) / initial_value

  return total_return

def calculate_max_drawdown(portfolio_data : pd.DataFrame) -> float:
  running_peak = portfolio_data['Total Value'].cummax()
  drawdowns = (portfolio_data["Total Value"] - running_peak)/ running_peak
  max_drawdown = drawdowns.min()

  return max_drawdown

def calculate_sharpe(portfolio_data : pd.DataFrame) -> float:
  pct_change = portfolio_data['Total Value'].pct_change()
  mean_daily_return = pct_change.mean()
  std_daily_return = pct_change.std()

  sr = (mean_daily_return / std_daily_return) * (252 ** 0.5)

  return sr


