import pytest
from portfolio_risk_analysis.portfolio import Portfolio, PortfolioValidationError
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_mock_stock_data(days):
  start_date = datetime.now() - timedelta(days=days)
  end_date = datetime.now()
  date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

  vals = np.ones(len(date_list))
  
  df = pd.DataFrame({"Close": vals, "Date": date_list})
  df.set_index(["Date"], inplace=True)
  return df

def mock_yfinance(mocked_ticker, num_days):
  mocked_instance = MagicMock()
  mocked_instance.history.return_value = create_mock_stock_data(num_days)
  mocked_ticker.return_value = mocked_instance


class TestPortfolioInit:
  def test_validate_cannot_be_empty(self):
    with pytest.raises(PortfolioValidationError) as err_info:
        Portfolio({}, "5y")
    assert str(err_info.value) == "Portfolio cannot be empty"

  def test_validate_must_allocate_100_percent(self):
    with pytest.raises(PortfolioValidationError) as err_info:
        Portfolio({ "MSFT": 90 }, "5y")
    assert str(err_info.value) == "Portfolio allocation does not sum to 100%, it sums to 90%"

    with pytest.raises(PortfolioValidationError) as err_info:
        Portfolio({ "MSFT": 101 }, "5y")
    assert str(err_info.value) == "Portfolio allocation does not sum to 100%, it sums to 101%"

  @patch("yfinance.Ticker")
  def test_portfolio_weights_are_stored_correctly(self, mocked_ticker):
    mock_yfinance(mocked_ticker, 365)
    p = Portfolio({"AAPL": 80, "MSFT": 20}, "1y")
    expected_weights = np.array([0.8, 0.2])
    assert np.all(np.equal(p.weights, expected_weights))


  @patch("yfinance.Ticker")
  def test_portfolio_df_is_created(self, mocked_ticker):
    num_days = 365
    mock_yfinance(mocked_ticker, num_days)
    p = Portfolio({"AAPL": 80, "MSFT": 20}, "1y")

    expected_columns = ["AAPL", "MSFT"]
    assert len(p.portfolio_df.columns) == len(expected_columns)
    assert all([actual == expected for actual, expected in zip(p.portfolio_df.columns, expected_columns)])

    assert len(p.portfolio_df["AAPL"]) == num_days + 1
    assert len(p.portfolio_df["MSFT"]) == num_days + 1

@patch("yfinance.Ticker")
def test_check_df_has_no_nan_values(mocked_ticker):
    mock_yfinance(mocked_ticker, 365)
    p = Portfolio({"AAPL": 100}, "1y")

    p.check_df_has_no_nan_values(p.portfolio_df)

    p.portfolio_df.loc[0, "AAPL"] = np.nan
    with pytest.raises(AssertionError):
        p.check_df_has_no_nan_values(p.portfolio_df)

@patch("yfinance.Ticker")
def test_calculate_volatility(mocked_ticker):
    mock_yfinance(mocked_ticker, 365)
    p = Portfolio({"AAPL": 40, "MSFT": 60}, "1y")

    returns_df = pd.DataFrame({"AAPL": [1, 2, 3], "MSFT": [6, 5, 4]})
    cov_matrix = returns_df.cov()
    
    expected_variance = np.dot(p.weights, np.dot(cov_matrix, p.weights))
    expected_volatility = np.sqrt(expected_variance)

    actual_volatility = p.calculate_volatility(cov_matrix)
    assert expected_volatility == actual_volatility
