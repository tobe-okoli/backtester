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

    short_sma = data['Close'].rolling(window=self.short_window).mean()
    long_sma = data["Close"].rolling(window=self.long_window).mean()

    signals = pd.Series(0, index=data.index)
    signals[short_sma > long_sma] = 1
    signals[short_sma < long_sma] = -1

    return signals
  
class DonchianChannelStrategy(Strategy):
  def __init__(self, window: int):
    self.window = window

  def generate_signals(self, data: pd.DataFrame) -> pd.Series:
    if len(data) < self.window:
      raise ValueError(f"Data length must be at least {self.window} for Donchian Channel calculation.")

    high = data['High'].rolling(window=self.window).max().shift(1)
    low = data['Low'].rolling(window=self.window).min().shift(1)

    signals = pd.Series(0, index=data.index)
    signals[data['Close'] > high] = 1
    signals[data['Close'] < low] = -1

    return signals

class BollingerBandsRSIStrategy(Strategy):
  def __init__(self, window: int, stdev: float, rsi_window: int, rsi_overbought: float, rsi_oversold: float):
    self.window = window
    self.stdev = stdev
    self.rsi_window = rsi_window
    self.rsi_overbought = rsi_overbought
    self.rsi_oversold = rsi_oversold

  def generate_signals(self, data: pd.DataFrame) -> pd.Series:
    if(len(data) < self.window or len(data) < self.rsi_window):
      raise ValueError(f"Data length must be at least {max(self.window, self.rsi_window)} for Bollinger Bands and RSI calculation.")

    # Calculate RSI

    daily_price_change = data['Close'].diff()
    gain = daily_price_change.where(daily_price_change > 0, 0)
    loss = -daily_price_change.where(daily_price_change < 0, 0)

    avg_gain = gain.rolling(window=self.rsi_window).mean()
    avg_loss = loss.rolling(window=self.rsi_window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100/(1 + rs))

    # Calculate Bollinger Bands
    rolling_std = data['Close'].rolling(window=self.window).std()

    mid_band = data['Close'].rolling(window=self.window).mean()
    upper_band = mid_band + (rolling_std * self.stdev)
    lower_band = mid_band - (rolling_std * self.stdev)

    signals = pd.Series(0, index=data.index)
    signals[(data['Close'] < lower_band) & (rsi < self.rsi_oversold)] = 1
    signals[(data['Close'] > upper_band) & (rsi > self.rsi_overbought)] = -1

    return signals

