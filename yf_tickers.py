import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import yfinance as yf
from finpandas import Stocks
from finpandas.utils import get_profile_by_ticker
from tqdm import tqdm


def yf_wrapper(tickers:list, start:str, end:str) -> pd.DataFrame:
    """
    query historical closing price for tickers every day in period

    Args:
        tickers (list): list of stock tickers strings, i.e ["AAPL", "SPY"]
        start (str): start date of period
        end (str): end date of period 

    Returns:
        pd.DataFrame: historical EOD data
    """    
    return yf.download(tickers, start=start, end=end, group_by = "ticker").reset_index()
    
    

def price_upload(tickers_filepath:str, start:str, end:str) -> pd.DataFrame:
    """
    uploads closing price of tickers in file to AWS database

    Args:
        tickers_filepath (str): filepath to json with tickers
        start (str): start date of period
        end (str): end date of period 

    Returns:
        pd.DataFrame: formatted dataframe that was uploaded to mysql
    """
    
    # ~~~~~~ all companies ~~~~~~ #
    # with open(tickers_filepath) as f:
    #     ticker_data = json.load(f)
    #     tickers = list(ticker_data.keys())


    # ~~~~~~~~~~~ s&p 500 companies ~~~~~~~~~~~ #
    tickers = [ticker.replace(".", "-") for ticker in pd.read_csv(tickers_filepath)["Symbol"].tolist()]
    names = pd.read_csv(tickers_filepath)["Name"].tolist()

    # format pandas df for upload
    data = yf_wrapper(tickers, start, end)
    new_df = pd.DataFrame(columns = ["open", "high", "low", "close", "adjclose", "volume", "date", "uom", "ticker", "cik", "name"])

    for i in tqdm(range(len(tickers))):
        ticker, name = tickers[i], names[i]
        temp_df = data[ticker][["Open", "High", "Low", "Close", "Adj Close", "Volume"]]
        temp_df.rename(columns = {"Open":"open", "High":"high", "Low":"low", "Close":"close", "Adj Close":"adjclose", "Volume":"volume"}, inplace = True)
        temp_df["date"] = data["Date"]
        temp_df["uom"] = "USD"
        try:
            cik, _, _ = get_profile_by_ticker(ticker)
        except TypeError:
            print(ticker, name)
        temp_df["ticker"] = ticker
        temp_df["cik"] = cik
        temp_df["name"] = name
        new_df = new_df.append(temp_df)

    to_upload = new_df.reset_index().drop("index", axis=1)
    
    # ~~~~~~~~ upload to MySQL database ~~~~~~~ #
    # i = Stocks(username, password)
    # i._commitdb("historical_eod", to_upload)

    return to_upload



def sector_upload(filepath:str) -> pd.DataFrame:
    """
    upload company sector data to AWS database

    Args:
        filepath (str): filepath to constituent information

    Returns:
        pd.DataFrame: formatted dataframe that was uploaded to mysql
    """    
    df = pd.read_csv(filepath)
    ciks = []
    for ticker in df["Symbol"]:
        ticker = ticker.replace(".", "-")
        try:
            ciks.append(get_profile_by_ticker(ticker)[0])
        except TypeError:
            print(ticker)
    df["CIK"] = ciks
    df.columns = ["ticker", "name", "sector", "cik"]

    # ~~~~~~~~ upload to MySQL database ~~~~~~~ #
    # i = Stocks(username, password)
    # i._commitdb("sector", df)

    return df


# if __name__ == "__main__":
    # filepath = Path(__file__).resolve().parent.joinpath('finpandas', 'resources', 'ticker.json')
    # sector_upload(filepath)

    # filepath = Path(__file__).resolve().parent.joinpath('finpandas', 'resources', 'constituents.csv')
    # print(close_upload(filepath, start="2021-02-08", end="2021-02-09"))
