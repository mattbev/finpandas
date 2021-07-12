"""
Custom errors.
"""

class TickerNotFoundError(Exception):
    """
    Exception raised when the inputted ticker is not found

    Args:
        ticker (str): the ticker
        message (str, optional): printed output. Defaults to
            "the inputted ticker '{ticker}' could not be found".
    """
    def __init__(self, ticker:str, message="inputted ticker '{ticker}' could not be found"):
        self.ticker = ticker
        self.message = message.format(ticker=self.ticker)
        super().__init__(self.message)


class NestedDepthError(Exception):
    """
    Exception raised when the inputted nested iterable is the incorrect depth

    Args:
        input_depth (int): the depth of the inputted iterable
        correct_depth (int): the correct depth of the inputted iterable
        message (str, optional): printed output. Defaults to
            "the nested depth of the iterable ({input_depth}) is invalid
            for required depth ({correct_depth})".
    """
    def __init__(self, input_depth:int, correct_depth:int,
        message="iterable depth of ({input_depth}) invalid for required depth ({correct_depth})"):
        self.input_depth = input_depth
        self.correct_depth = correct_depth
        self.message = message.format(
            input_depth=self.input_depth,
            correct_depth=self.correct_depth
            )
        super().__init__(self.message)
