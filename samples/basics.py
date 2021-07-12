from finpandas import dispose, fundamentals, stocks

company = 'AAPL'

form = fundamentals.ten_k(company, years=[2018, 2019])
stocks = stocks.price(company, period_start='2018-01-01', period_end='2019-12-31')

print(form)
print(stocks)

dispose()