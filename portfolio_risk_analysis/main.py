from portfolio import Portfolio

all_apple = { "AAPL": 100 }
mixed = {
  "AAPL": 35,
  "MSFT": 20,
  "TSLA": 5,
  "C": 5,
  "GS": 5,
  "SPCE": 30
}
volatile = {
  "VINC": 50,
  "MGAM": 50
}
portfolio = Portfolio(volatile, "1y")

portfolio.calculate_portfolio_volatility()
