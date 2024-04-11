from portfolio import Portfolio
import matplotlib.pyplot as plt

all_apple = { "AAPL": 100 }
mixed = {
  "AAPL": 25,
  "MSFT": 5,
  "TSLA": 5,
  "C": 5,
  "GS": 30,
  "SPCE": 30
}
volatile = {
  "VINC": 50,
  "MGAM": 50,
}
portfolio = Portfolio(mixed, "5y")

portfolio_volatility = portfolio.calculate_portfolio_volatility() * 100
print(f"Portfolio volatility: {portfolio_volatility}%")

monthly_volatility = portfolio.calculate_portfolio_volatility_against_time() * 100
monthly_volatility.plot(title="Monthly Volatility Vs Time")
plt.xlabel('Date')
plt.ylabel('Volatility(%)')
plt.show()
