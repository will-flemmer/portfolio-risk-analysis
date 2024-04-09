import pytest
from portfolio_risk_analysis.portfolio import Portfolio, PortfolioValidationError

def test_validate_cannot_be_empty():
  with pytest.raises(PortfolioValidationError) as err_info:
      Portfolio({})
  assert str(err_info.value) == "Portfolio cannot be empty"

def test_validate_must_allocate_100_percent():
  with pytest.raises(PortfolioValidationError) as err_info:
      Portfolio({ "MSFT": 90 })
  assert str(err_info.value) == "Portfolio allocation does not sum to 100%, it sums to 90%"
  with pytest.raises(PortfolioValidationError) as err_info:
      Portfolio({ "MSFT": 101 })
  assert str(err_info.value) == "Portfolio allocation does not sum to 100%, it sums to 101%"