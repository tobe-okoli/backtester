import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "engine"))


from execution import Execution
from portfolio import Portfolio
from strategy import SMAStrategy

import pandas as pd
import time
import statistics 



def benchmark_portfolio(path):

  raw_csv = pd.read_csv(path)

  date_col = "Date" if "Date" in raw_csv.columns else "Datetime"

  data = pd.read_csv(path, parse_dates=[date_col], index_col=date_col)
  strategy = SMAStrategy(short_window=50, long_window=100)
  signals = strategy.generate_signals(data)
  execution = Execution(slippage=0.01, commission=0.001)
  portfolio = Portfolio(data, signals, 10000, execution)

  times = []

  for i in range(5):
    portfolio = Portfolio(data, signals, 10000, execution)
    start = time.perf_counter()
    portfolio.simulate_trades()
    end = time.perf_counter()

    elapsed_time = end - start

    times.append(elapsed_time)

  median_time = statistics.median(times)

  bars_per_second = len(data) / median_time

  print(f"Row count: {len(data)}")
  print(f"Median time: {median_time:.6f} seconds")
  print(f"Bars per second: {bars_per_second:.2f}")

if __name__ == "__main__":
  #benchmark_portfolio("benchmarks/data/AAPL_1d.csv")
  #benchmark_portfolio("benchmarks/data/AAPL_1h.csv")
  #benchmark_portfolio("benchmarks/data/AAPL_5m.csv")

  benchmark_portfolio("benchmarks/data/synthetic_10000.csv")
  benchmark_portfolio("benchmarks/data/synthetic_100000.csv")
  benchmark_portfolio("benchmarks/data/synthetic_1000000.csv")
