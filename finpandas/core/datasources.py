"""
Used for analysis of public companies filing with the
United States SEC.
"""

from dataclasses import dataclass
from typing import Iterable, Tuple, Union

import pandas as pd

from ..dataframes import Form10K, Form10Q, HistoricalStockPrices
from ..utils import NestedDepthError, nested_depth, ticker_or_cik_parser
from .connections import DatabaseConnection


@dataclass
class Fundamentals(DatabaseConnection):
    """
    Fundamentals API

    Args:
        database (str, optional): database to connect to. Defaults to 'xbrl'.
    """

    database: str = "xbrl"


    def ten_k(self, ticker_or_cik:Union[str,int], years:Union[int,Iterable[int]]) -> Form10K:
        """
        get company 10-Ks for selected years

        Args:
            ticker_or_cik (Union[str,int]): company's ticker or SEC issued Central Index Key (CIK)
            years (Union[int,Iterable[int]]): a year or iterable of years of interest

        Returns:
            Form10K: a representation of the company's 10Ks
        """
        cik = ticker_or_cik_parser(ticker_or_cik)

        if isinstance(years, int):
            year_where_clause = f"fy={years}"
        elif len(years) == 1:
            year_where_clause = f"fy={years[0]}"
        else:
            year_where_clause = f"fy IN {tuple(years)}"

        command = ("SELECT a.fy, a.fye, b.tag, b.value, b.uom, b.ddate "
                   "FROM num b JOIN sub a ON a.adsh=b.adsh "
                   f"WHERE cik={cik} AND form='10-K' AND {year_where_clause}")

        return Form10K(pd.read_sql_query(command, self.engine))


    def ten_q(
        self,
        ticker_or_cik:Union[str,int],
        periods:Union[int,Iterable[int],Tuple[Union[str,int],Union[str,int]],
            Iterable[Tuple[Union[str,int],Union[str,int]]]]
        ) -> Form10Q:
        """
        get company 10-Qs for selected periods

        Args:
            ticker_or_cik (Union[str,int]): company's ticker or SEC issued Central Index Key (CIK)
            periods (Union[int,Iterable[int],Tuple[Union[str,int],Union[str,int]],\
                Iterable[Tuple[Union[str,int],Union[str,int]]]]): the year of interest, will get all
                quarters; years of interest, will get all quarters; (year, quarter) pair;
                (year, quarter) pairs of interest

        Raises:
            NestedDepthError: inputted periods is not one of the correct formats

        Returns:
            Form10Q: a representation of the company's 10Qs

        Example:
            Querying 10-Q reports for Apple Inc.::

                instance = Fundamentals(username, password)
                df = instance.query_10Q("AAPL", 2019)
                df = instance.query_10Q("AAPL", [2018, 2019])
                df = instance.query_10Q("AAPL", (2019, "q1"))
                df = instance.query_10Q("AAPL", [(2019, "q1"), (2019, "q2")]
        """
        cik = ticker_or_cik_parser(ticker_or_cik)

        depth = nested_depth(periods)
        if depth == 0:
            periods = [(periods, quarter) for quarter in ["q1", "q2", "q3", "q4"]]
        elif depth == 1:
            if isinstance(periods, tuple):
                periods = [periods]
            else:
                periods = [(year,quarter) for year in periods for quarter in ["q1","q2","q3","q4"]]
        elif depth > 2:
            raise NestedDepthError(input_depth=depth, correct_depth=[0, 1, 2])


        period_where_clause = "(" + \
            "".join(
            f"(a.fy={year} AND a.fp='{quarter}') OR " for year,quarter in periods)[:-4] + \
            ")"

        command = ("SELECT a.fy, a.fp, b.tag, b.value, b.uom, b.ddate "
                   "FROM num b JOIN sub a ON a.adsh=b.adsh "
                   f"WHERE cik={cik} AND form='10-Q' AND {period_where_clause}")

        return Form10Q(pd.read_sql_query(command, self.engine))



@dataclass
class Stocks(DatabaseConnection):
    """
    Stocks API

    Args:
        database (str, optional): database to connect to. Defaults to 'stocks'.
    """

    database: str = "stocks"


    def price(
        self,
        ticker_or_cik:Union[str,int],
        period_start:str,
        period_end:str=None
        ) -> pd.DataFrame:
        """
        queries the price of a given equity over a period

        Args:
            ticker_or_cik (Union[str,int]): company or fund's ticker or SEC
                issued Central Index Key (CIK)
            period_start (str): the starting day for the period,
                in year-month-day format (e.g. 2020-06-30).
            period_end (str, optional): the ending day for the period,
                in year-month-day format (e.g. 2020-06-30). Defaults to None,
                indicating a single day period_start.

        Returns:
            pd.DataFrame: a representation of the company's historical stock price
        """
        cik = ticker_or_cik_parser(ticker_or_cik)
        if period_end is None:
            period_end = period_start

        command = (f"SELECT * from historical_eod WHERE cik={cik} "
                   f"AND date BETWEEN '{period_start}' AND '{period_end}'")

        return HistoricalStockPrices(pd.read_sql_query(command, self.engine))


    def sector(self, ticker_or_cik:Union[str,int]) -> str:
        """
        queries the sector of a given entity

        Args:
            ticker_or_cik (Union[str,int]): company or fund's ticker or SEC
                issued Central Index Key (CIK)

        Returns:
            str: the sector
        """
        cik = ticker_or_cik_parser(ticker_or_cik)

        command = (f"SELECT sector from sector WHERE cik={cik}")

        return pd.read_sql_query(command, self.engine).squeeze()
