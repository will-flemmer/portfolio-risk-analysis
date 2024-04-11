import yfinance as yf
import pandas as pd
import numpy as np

class PortfolioValidationError(Exception):
  pass

class Portfolio():
  def __init__(self, stock_portions, time_period):
    self.stock_portions = stock_portions
    self.validate()
    self.time_period = time_period
    self.weights = np.array([x / 100 for x in self.stock_portions.values()])
    self.create_portfolio_df()

  def validate(self):
    if not bool(self.stock_portions):
      raise PortfolioValidationError("Portfolio cannot be empty")
    total_percentage_alloc = sum(self.stock_portions.values())
    if total_percentage_alloc != 100:
      raise PortfolioValidationError(f"Portfolio allocation does not sum to 100%, it sums to {total_percentage_alloc}%")
  
  def create_portfolio_df(self):
    close_prices = {}
    for stock_symbol in self.stock_portions.keys():
      close_prices[stock_symbol] = yf.Ticker(stock_symbol).history(period=self.time_period)['Close']

    self.portfolio_df = pd.DataFrame(close_prices)

  def calculate_portfolio_volatility_against_time(self):
    window_size_days = 30
    returns_df = self.daily_returns_df()
    volatility_df = returns_df.rolling(window_size_days).std().dropna()

    for end in range(window_size_days, len(returns_df) + 1):
      monthly_returns_df = returns_df[end - window_size_days: end]
      date_index = monthly_returns_df.tail(1).index
      cov_matrix = self.create_covariance_matrix(monthly_returns_df)
      volatility = self.calculate_volatility(cov_matrix)
      volatility_df.loc[date_index, "Portfolio"] = volatility

    self.check_df_has_no_nan_values(returns_df)
    return volatility_df

  def calculate_portfolio_volatility(self):
    cov_matrix = self.create_covariance_matrix(self.daily_returns_df())
    return self.calculate_volatility(cov_matrix)
  
  def calculate_volatility(self, cov_matrix):
    portfolio_variance = np.dot(self.weights, np.dot(cov_matrix, self.weights))
    return np.sqrt(portfolio_variance)

  def create_covariance_matrix(self, returns_df):
    self.check_df_has_no_nan_values(returns_df)
    return returns_df.cov()
  
  def daily_returns_df(self):
    return self.portfolio_df.pct_change().dropna()
  
  def check_df_has_no_nan_values(self, df):
    assert(df[df.isna().any(axis=1)].empty) == True