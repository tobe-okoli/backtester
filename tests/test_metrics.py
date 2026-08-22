import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "engine"))

from metrics import calculate_total_return, calculate_max_drawdown, calculate_sharpe


def test_total_return_positive_case():
    data = pd.DataFrame({"Total Value": [10000, 11000]})
    result = calculate_total_return(data)
    assert result == 0.1


def test_total_return_negative_case():
    data = pd.DataFrame({"Total Value": [10000, 9000]})
    result = calculate_total_return(data)
    assert result == -0.1


def test_total_return_no_change():
    data = pd.DataFrame({"Total Value": [10000, 10000]})
    result = calculate_total_return(data)
    assert result == 0.0


def test_max_drawdown_simple_drop():
    data = pd.DataFrame({"Total Value": [10000, 12000, 8000, 9000]})
    result = calculate_max_drawdown(data)
    assert round(result, 4) == round((8000 - 12000) / 12000, 4)


def test_max_drawdown_no_drop():
    data = pd.DataFrame({"Total Value": [10000, 11000, 12000]})
    result = calculate_max_drawdown(data)
    assert result == 0.0


def test_sharpe_runs_without_error():
    data = pd.DataFrame({"Total Value": [10000, 10100, 10050, 10200, 10300]})
    result = calculate_sharpe(data)
    assert isinstance(result, float)
