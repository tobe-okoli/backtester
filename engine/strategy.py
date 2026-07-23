import pandas as pd

class Strategy:
  def generate_signals(self,data: pd.DataFrame) -> pd.Series:
    raise NotImplementedError("Subclasses should implement this method.")

class SMAStrategy(Strategy):
  def   __init__(self, short_window: int, long_window: int):
    self.short_window = short_window
    self.long_window = long_window


  def generate_signals(self, data: pd.DataFrame) -> pd.Series:

    if len(data) < self.long_window:
      raise ValueError(f"Data length must be at least {self.long_window} for SMA calculation.")

    short_sma = data['Close'].rolling(window=self.short_window, min_periods=1).mean()
    long_sma = data["Close"].rolling(window=self.long_window).mean()

    signals = pd.Series(0, index=data.index)
    signals[short_sma > long_sma] = 1
    signals[short_sma < long_sma] = -1

    return signals
  

