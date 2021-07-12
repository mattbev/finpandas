# finpandas
Toolkit for U.S. public sector financial analysis. Compare multiple companies across multiple years, in seconds, without having to download data locally. 

## About
**fundamentals:** for United States public fundamentals (10-Ks, 10-Qs, etc.) filed with the SEC.

**stocks:** for historical stock pricing information on United States public companies.

[Documentation](https://mattbeveridge.com/blacktip-docs)

## Installation
`finpandas` can be installed from PyPI using `pip`:
```
pip install finpandas
```
and from source [here](): TODO

## Usage
The workflow is the following:

**Import.**
```python
from finpandas import fundamentals, stocks, dispose
```

**Get data.**
```python
# examine 10-K filings
form10k = fundamentals.ten_k("AAPL", 2019)
form10ks = fundamentals.ten_k("aapl", [2016, 2017, 2018])

# examine 10-Q filings
form10q = fundamentals.ten_q("tsla", (2018, "Q3"))
form10qs = fundamentals.ten_q("TSLA", [(2017, "Q1"), (2016, "Q2")])
form10qs = fundamentals.ten_q("tsla", [2016, 2017, 2018])

# examine historical stock prices
stock_prices = stocks.prices("aapl", "2018-01-01", "2020-12-31")
```


**Manipulate the data.**
```python
# example calculations
balance_sheet = form10k.balance_sheet()
roe = form10qs.return_on_equity()
net_income = form10k.net_income()
search = form10k.search("Amortization")
```

**Get data _efficiently_ (multithreading).**

The largest efficiency bottleneck is the I/O speed, which is reduced through parallelized queries. 
```python
from finpandas.utils import Jobs

# add jobs to the queue
jobs = Jobs()
jobs.add_job(fundamentals.ten_k, "aapl", [2017, 2018, 2019])
jobs.add_job(fundamentals.ten_q, "fb", 2010)

# execute the queries
results = jobs.execute()
```

**Close your connection.**
```python
dispose()
```

For further examples, see [samples](samples).
