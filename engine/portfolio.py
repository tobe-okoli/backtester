import pandas as pd
from execution import Execution
import numpy as np

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

    close_prices = self.data['Close'].to_numpy()
    signals = self.signals.to_numpy()

    for i in range(len(close_prices)):
      todays_signal = signals[i]
      close_price = close_prices[i]
      if todays_signal == 1:
        price = self.execution.calculate_trade_price(close_price, 1)

        shares_to_buy = cash // price
        shares += shares_to_buy
        cash -= shares_to_buy * price

      elif todays_signal == -1:
        price = self.execution.calculate_trade_price(close_price, -1)

        cash += shares * price
        shares = 0
      else:
        pass

      total_value = cash + shares * close_price
      history.append(total_value)

    return pd.DataFrame(history, index=self.data.index, columns=['Total Value'])
