"""
finpandas package.

Used to analyze SEC fundamental data. 
"""

from .core import Fundamentals, Stocks

fundamentals = Fundamentals()
stocks = Stocks()

def dispose():
    fundamentals.dispose()
    stocks.dispose()

__all__ = [
    "fundamentals",
    "stocks",
]
