"""
helper functions
"""

import json
from pathlib import Path
from typing import Iterable, Tuple, Union

import dpath.util

from .errors import TickerNotFoundError


class SafeList(list):
    """
    subclass of list datatype that allows safe indexing
    """
    def get(self, index:int, default:object=None) -> object:
        """
        safe indexing method

        Args:
            index (int): [description]
            default (object, optional): what to return if indexing fails. Defaults to None.

        Returns:
            object: either the value at that index or a default value
        """
        try:
            return self.__getitem__(index)
        except IndexError:
            return default


def get_profile_by_cik(cik:Union[str,int]) -> Union[None,Tuple[int,str,str]]:
    """
    gets the company profile using the CIK number

    Args:
        cik (Union[str,int]): the SEC issued Central Index Key (CIK)

    Returns:
        Union[None,Tuple[int,str,str]]: (cik, ticker, title)
    """
    path = Path(__file__).resolve().parent.parent.joinpath('resources', 'cik.json')
    cik_json = json.load(open(path))
    result = cik_json.get(str(cik), None)
    if result is None:
        return result
    return tuple(result.values())


def get_profile_by_ticker(ticker:str) -> Union[None,Tuple[int,str,str]]:
    """
    gets the company profile using the ticker

    Args:
        ticker (str): the ticker of the company

    Returns:
        Union[None,Tuple[int,str,str]]: (cik, ticker, title)
    """
    path = Path(__file__).resolve().parent.parent.joinpath('resources', 'ticker.json')
    ticker_json = json.load(open(path))
    result = ticker_json.get(ticker.upper(), None)
    if result is None:
        return result
    return tuple(result.values())


def get_profile_by_title(title:str) -> Union[None,Tuple[int,str,str],
    Iterable[Tuple[int,str,str]]]:
    """
    gets the company profile using the title

    Args:
        title (str): the company's name in glob form

    Returns:
        Union[None,Tuple[int,str,str],Iterable[Tuple[int,str,str]]]: (cik, ticker, title)
    """
    path = Path(__file__).resolve().parent.parent.joinpath('resources', 'title.json')
    title_json = json.load(open(path))
    result = dpath.util.values(title_json, title)
    if len(result) == 0:
        return None
    if len(result) == 1:
        return tuple(result[0].values())
    return tuple(tuple(i.values()) for i in result)


def ticker_or_cik_parser(ticker_or_cik:Union[str,int]) -> int:
    """
    takes in a ticker or CIK number and returns just the CIK number.
    a convenience function for internal use.

    Args:
        ticker_or_cik (Union[str,int]): ticker or SEC issued Central Index Key (CIK)

    Raises:
        TickerNotFoundError: if the ticker is not found in our database

    Returns:
        int: the CIK number
    """
    if isinstance(ticker_or_cik, int):
        cik = ticker_or_cik
    elif len(str(ticker_or_cik)) != 10 and \
        str([s for s in ticker_or_cik if s.isdigit()]) != str(ticker_or_cik):
        # check if input is a ticker or a CIK. CIKs are 10 digit numbers,
        # tickers are <= 5 character alphanumeric strings
        # if this if statement is true, then the input is a ticker
        ticker = ticker_or_cik
        profile_results = get_profile_by_ticker(ticker)
        if profile_results is None:
            raise TickerNotFoundError(ticker)
        cik, _, _ = profile_results
    else:
        cik = ticker_or_cik

    return int(cik)


def nested_depth(iterable:Iterable) -> int:
    """
    calculate the nested depth of an iterable

    Args:
        iterable (Iterable): the iterable to calculate the depth of

    Returns:
        int: the depth
    """
    depth_func = lambda L: isinstance(L, (list, tuple)) and max(map(depth_func, L)) + 1
    depth = depth_func(iterable)
    return depth if depth is not False else 0


def count_object_methods(obj:object):
    """
    get the number of callable object methods

    Args:
        obj (object): any object

    Returns:
        int: the number of object class methods
    """
    return len([k for k,v in obj.__dict__.items() if callable(v)])