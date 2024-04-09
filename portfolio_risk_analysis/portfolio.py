
class PortfolioValidationError(Exception):
  pass

class Portfolio():
  def __init__(self, stock_portions):
    self.stock_portions = stock_portions
    self.validate()

  def validate(self):
    if not bool(self.stock_portions):
      raise PortfolioValidationError("Portfolio cannot be empty")
    total_percentage_alloc = sum(self.stock_portions.values())
    if total_percentage_alloc != 100:
      raise PortfolioValidationError(f"Portfolio allocation does not sum to 100%, it sums to {total_percentage_alloc}%")

