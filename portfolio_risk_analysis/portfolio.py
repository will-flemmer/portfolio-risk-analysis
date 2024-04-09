import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class PortfolioValidationError(Exception):
  pass

class Portfolio():
  def __init__(self, stock_portions, time_period):
    self.stock_portions = stock_portions
    self.time_period = time_period
    self.validate()

  def validate(self):
    if not bool(self.stock_portions):
      raise PortfolioValidationError("Portfolio cannot be empty")
    total_percentage_alloc = sum(self.stock_portions.values())
    if total_percentage_alloc != 100:
      raise PortfolioValidationError(f"Portfolio allocation does not sum to 100%, it sums to {total_percentage_alloc}%")

  def calculate_portfolio_volatility(self):
    cov_matrix = self.create_covariance_matrix()
    weights = np.array([x / 100 for x in self.stock_portions.values()])
    portfolio_volatility = np.sqrt(np.dot(weights, np.dot(cov_matrix, weights)))
    print(f"Portfolio volatility: {portfolio_volatility * 100}%")

  def create_covariance_matrix(self):
    close_prices = {}
    for stock_symbol in self.stock_portions.keys():
      close_prices[stock_symbol] = yf.Ticker(stock_symbol).history(period=self.time_period)['Close']

    stock_df = pd.DataFrame(close_prices)
    stock_df = stock_df.pct_change().dropna()

    # This line ensures there are no NaN values in stock_df
    assert(stock_df[stock_df.isna().any(axis=1)].empty) == True

    return stock_df.cov()