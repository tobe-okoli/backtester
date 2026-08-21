import pandas as pd
from execution import Execution

class Portfolio:
  def __init__(self, data: pd.DataFrame, signals: pd.Series, initial_cash: float, execution: Execution):
    self.data = data
    self.signals = signals
    self.initial_cash = initial_cash
    self.execution = execution

  
  def simulate_trades(self) -> pd.DataFrame:
    cash: float = self.initial_cash
    shares: int = 0
    total_value: float = cash
    history = []

    for date, row in self.data.iterrows():
      todays_signal = self.signals.get(date, 0)
      
      if todays_signal == 1:
        price = self.execution.calculate_trade_price(row['Close'], 1)

        shares_to_buy = cash // price
        shares += shares_to_buy
        cash -= shares_to_buy * price

      elif todays_signal == -1:
        price = self.execution.calculate_trade_price(row['Close'], -1)

        cash += shares * price
        shares = 0
      else:
        pass

      total_value = cash + shares * row['Close']
      history.append(total_value)

    return pd.DataFrame(history, index=self.data.index, columns=['Total Value'])
