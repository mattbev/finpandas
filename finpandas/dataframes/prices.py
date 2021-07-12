"""
Abstract data types for historical pricing.
"""

import pandas as pd


# pylint: disable=too-many-ancestors
class HistoricalPrices(pd.DataFrame):
    """
    Abstract Data Type for historical prices.
    Subclass of pandas DataFrame.
    """
    def __init__(self, dataframe:pd.DataFrame):
        """
        Args:
            dataframe (pd.DataFrame): the historical data content
        """
        super().__init__(self._format(dataframe))


    @property
    def _constructor(self):
        return HistoricalPrices


    @property
    def _constructor_sliced(self):
        return pd.Series


    @property
    def _constructor_expanddim(self):
        return HistoricalPrices


    @staticmethod
    def _format(dataframe:pd.DataFrame) -> pd.DataFrame:
        return dataframe



class HistoricalStockPrices(HistoricalPrices):
    """
    Abstract Data Type for historical stock prices
    """
    @staticmethod
    def _format(dataframe:pd.DataFrame) -> pd.DataFrame:
        """
        group source content into a usable format

        Args:
            dataframe (pd.DataFrame): the raw content

        Returns:
            pd.DataFrame: the formatted content
        """
        dataframe = dataframe.drop(["cik", "name"], axis=1)
        dataframe["date"] = dataframe["date"].map(lambda x: x.strftime('%Y-%m-%d'))
        return dataframe.set_index("ticker", drop=True)
