import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "engine"))

from strategy import SMAStrategy, Strategy


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