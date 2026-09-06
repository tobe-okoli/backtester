import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "engine"))

from strategy import SMAStrategy, DonchianChannelStrategy, BollingerBandsRSIStrategy, Strategy


def test_base_strategy_raises_not_implemented():
    strategy = Strategy()
    data = pd.DataFrame({"Close": [1, 2, 3]})
    try:
        strategy.generate_signals(data)
        assert False, "expected NotImplementedError but nothing was raised"
    except NotImplementedError:
        pass


def test_sma_strategy_generates_buy_signal_after_price_jump():
    prices = [100] * 10 + [200] * 10
    data = pd.DataFrame({"Close": prices})

    strategy = SMAStrategy(short_window=3, long_window=10)
    signals = strategy.generate_signals(data)
    
    assert signals.iloc[12] == 1


def test_sma_strategy_raises_when_data_too_short():
    data = pd.DataFrame({"Close": [100, 101, 102]})
    strategy = SMAStrategy(short_window=3, long_window=10)

    try:
        strategy.generate_signals(data)
        assert False, "expected ValueError but nothing was raised"
    except ValueError:
        pass

def test_donchian_breakout_generates_buy_signal():
    highs = [100, 101, 102, 103, 104, 110]
    lows = [90, 91, 92, 93, 94, 100]
    close = [95, 96, 97, 98, 99, 109]

    data = pd.DataFrame({"High": highs, "Low": lows, "Close": close})
    strategy = DonchianChannelStrategy(window=3)
    signals = strategy.generate_signals(data)

    assert signals.iloc[-1] == 1


def test_donchian_breakdown_generates_sell_signal():
    highs = [100, 101, 102, 103, 104, 105]
    lows = [90, 91, 92, 93, 94, 85]
    close = [95, 96, 97, 98, 99, 89]

    data = pd.DataFrame({"High": highs, "Low": lows, "Close": close})
    strategy = DonchianChannelStrategy(window=3)
    signals = strategy.generate_signals(data)

    assert signals.iloc[-1] == -1

def test_bollinger_rsi_generates_buy_signal():
    close = [100, 101, 102, 103, 60]
    data = pd.DataFrame({"Close": close})
    strategy = BollingerBandsRSIStrategy(window=3, stdev=1, rsi_window=3, rsi_overbought=70, rsi_oversold=30)
    signals = strategy.generate_signals(data)

    assert signals.iloc[-1] == 1

def test_bollinger_rsi_generates_sell_signal():
    close = [100, 101, 102, 103, 160]
    data = pd.DataFrame({"Close": close})
    strategy = BollingerBandsRSIStrategy(window=3, stdev=1, rsi_window=3, rsi_overbought=70, rsi_oversold=30)
    signals = strategy.generate_signals(data)

    assert signals.iloc[-1] == -1
