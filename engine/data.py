import pandas as pd
import yfinance as yf

def fetch_stock_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
  if start_date >= end_date:
    raise ValueError("Start date must be earlier than end date.")
  
  stock_data = yf.download(ticker, 
  start=start_date, end=end_date)
  stock_data.columns = stock_data.columns.droplevel("Ticker")

  if stock_data.empty:
    raise ValueError(f"No data found for ticker {ticker} between {start_date} and {end_date}.")

  return stock_data