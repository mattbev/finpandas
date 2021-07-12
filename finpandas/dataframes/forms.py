"""
Abstract data types for US public fundamentals: 10K and 10Q.
"""
import regex as re

import pandas as pd


# pylint: disable=too-many-public-methods
# pylint: disable=too-many-ancestors
class Form(pd.DataFrame):
    """
    Abstract Data Type for SEC forms. Subclass of pandas DataFrame.
    """
    def __init__(self, dataframe:pd.DataFrame):
        """
        Args:
            dataframe (pd.DataFrame): the form content
        """
        super().__init__(self._format(dataframe))


    @property
    def _constructor(self):
        return Form


    @property
    def _constructor_sliced(self):
        return pd.Series


    @property
    def _constructor_expanddim(self):
        return Form


    @staticmethod
    def _format(dataframe:pd.DataFrame) -> pd.DataFrame:
        return dataframe

    
    def search(self, regex:str, index:str="tag", axis:int=0) -> pd.DataFrame:   
        """
        generates a data sheet based on a keyword regex

        Args:
            regex (str): the keyword regular expression
            index (str, optional): dataframe index to search along 
                ("tag", "uom", "fy", "fp", etc.). Defaults to "tag".
            axis (int, optional): the axis the index belongs to 
                ("tag", "uom" on 0, "fy", "fp" on 1). Defaults to 0.

        Returns:
            pd.DataFrame: subset of the whole dataframe filtered by the regex
        """
        # return self.loc[self.index.get_level_values(index).str.contains(regex)] # old
        matcher = re.compile(regex)
        f = lambda x: matcher.search(str(x)) is not None
        values = self.axes[axis].get_level_values(index).map(f)
        return self.loc(axis=axis)[values]



    def asset_sheet(self) -> pd.DataFrame:
        """
        generates a data sheet of "Asset" values

        Returns:
            pd.DataFrame: subset of the whole dataframe filtered by assets
        """
        return self.search("Asset|Assets")


    def liability_sheet(self) -> pd.DataFrame:
        """
        generates a data sheet of "Liability" values

        Returns:
            pd.DataFrame: subset of the whole dataframe filtered by liabilities
        """
        return self.search("Liability|Liabilities")


    def debt_sheet(self) -> pd.DataFrame:
        """
        generates a data sheet of "Debt" values

        Returns:
            pd.DataFrame: subset of the whole dataframe filtered by debts
        """
        return self.search("Debt|Debts")


    def balance_sheet(self) -> pd.DataFrame:
        """
        TODO:
            generates the balance sheet

        Returns:
            pd.DataFrame: subset of the whole dataframe filtered by values on a balance sheet
        """
        return self.copy()


    def cash_flow(self) -> pd.DataFrame:
        """
        TODO:
            generates the cash flow statement

        Returns:
            pd.DataFrame: subset of the whole dataframe filtered by values on a cash flow statement
        """
        return self.copy()


    def book_value(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates the book value = total assets - total liabilities

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the book values
        """
        assets = self.search("^Assets$")
        liabilities = self.search("^Liabilities$")
        years = assets.columns.to_list()
        dataframe = assets.reindex([("BookValue", "USD")])

        for year in years:
            dataframe[year] = assets[year][0] - liabilities[year][0]

        return dataframe.values[0] if as_list else dataframe


    def current_ratio(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates the current ratio = current assets / current liabilities

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the current ratio values
        """
        current_assets = self.search("^AssetsCurrent$")
        current_liabilities = self.search("^LiabilitiesCurrent$")
        years = current_assets.columns.to_list()
        dataframe = current_assets.reindex([("CurrentRatio", "ratio")])

        for year in years:
            dataframe[year] = current_assets[year][0] / current_liabilities[year][0]

        return dataframe.values[0] if as_list else dataframe


    def quick_ratio(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates the quick ratio = (current assets - inventory) / current liabilities

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the quick ratio values
        """
        current_assets = self.search("^AssetsCurrent$")
        inventory = self.search("^InventoryNet$")
        current_liabilities = self.search("^LiabilitiesCurrent$")
        years = current_assets.columns.to_list()
        dataframe = current_assets.reindex([("QuickRatio", "ratio")])

        for year in years:
            dataframe[year] = (current_assets[year][0] - inventory[year][0]) \
                / current_liabilities[year][0]

        return dataframe.values[0] if as_list else dataframe


    def return_on_assets(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates ROA = net income / average total assets

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the ROA values

        TODO:
            make sure values are interpreted correctly for 10Q/10K distinction
        """
        net_income = self.net_income()
        total_assets = self.search("^Assets$")
        years = net_income.columns.to_list()
        dataframe = net_income.reindex([("ReturnOnAssets", "ratio")])

        for year in years:
            dataframe[year] = net_income[year][0] / total_assets[year][0]

        return dataframe.values[0] if as_list else dataframe


    def return_on_equity(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates ROE = net income / total stockholders equity

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the ROE values

        TODO:
            make sure values are interpreted correctly for 10Q/10K distinction
        """
        net_income =  self.net_income()
        stockholders_equity = self.search("^StockholdersEquity$")
        years = net_income.columns.to_list()
        dataframe = net_income.reindex([("ReturnOnEquity", "ratio")])

        for year in years:
            dataframe[year] = net_income[year][0] / stockholders_equity[year][0]

        return dataframe.values[0] if as_list else dataframe


    def debt_to_equity(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates the debt-to-equity ratio = total liabilities / total stockholders equity

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the debt-to-equity ratio
        """
        total_liabilities = self.search("^Liabilities$")
        stockholders_equity = self.search("^StockholdersEquity$")
        years = total_liabilities.columns.to_list()
        dataframe = total_liabilities.reindex([("DebtToEquity", "ratio")])

        for year in years:
            dataframe[year] = total_liabilities[year][0] / stockholders_equity[year][0]

        return dataframe.values[0] if as_list else dataframe


    def debt_to_assets(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates the debt-to-equity ratio = total liabilities / total assets

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the debt-to-assets ratio
        """
        total_liabilities = self.search("^Liabilities$")
        total_assets = self.search("^Assets$")
        years = total_liabilities.columns.to_list()
        dataframe = total_liabilities.reindex([("DebtToAssets", "ratio")])

        for year in years:
            dataframe[year] = total_liabilities[year][0] / total_assets[year][0]

        return dataframe.values[0] if as_list else dataframe


    def ebit(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates EBIT = Net Income + Taxes

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the EBIT
        """
        # ebit = self.search(
        #     "^IncomeLossFromContinuingOperationsBefore"
        #     "IncomeTaxesExtraordinaryItemsNoncontrollingInterest$"
        # )
        ebit = self.search("^OperatingIncomeLoss$")
        years = ebit.columns.to_list()
        dataframe = ebit.reindex([("EBIT", "USD")])

        for year in years:
            dataframe[year] = ebit[year][0]

        return dataframe.values[0] if as_list else dataframe


    def ebitda(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates EBITDA = Net Income + Taxes + Depreciation + Amortization

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the EBITDA
        """
        ebit = self.ebit()
        depreciation_and_amortization_regexes = [
            "^DepreciationDepletionAndAmortization$",
            "DepreciationAmortizationAndImpairment"
        ]
        i = 0
        depreciation_and_amortization = self.search(
            depreciation_and_amortization_regexes[i]
        )
        while depreciation_and_amortization.empty:
            depreciation_and_amortization = self.search(
                depreciation_and_amortization_regexes[i]
            )
            i += 1
        # if depreciation_and_amortization.empty:
        #     # depreciation_and_amortization = self.search("(?=.*Depreciation)(?=.*Amortization)")
        #     depreciation_and_amortization = self.search(
        #         "DepreciationAmortizationAndImpairmentOnDisposit"
        #     )
        years = ebit.columns.to_list()
        dataframe = ebit.reindex([("EBITDA", "USD")])

        for year in years:
            dataframe[year] = ebit[year][0] + depreciation_and_amortization[year][0]

        return dataframe.values[0] if as_list else dataframe


    def gross_margin(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates gross margin

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the gross margin
        """
        gross_margin = self.search("^GrossProfit$")
        years = gross_margin.columns.to_list()
        dataframe = gross_margin.reindex([("GrossMargin", "USD")])

        for year in years:
            dataframe[year] = gross_margin[year][0]

        return dataframe.values[0] if as_list else dataframe


    def debt_capitalization(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates debt capitalization = liabilities / (liabilities + stockholder equity)

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the debt capitalization
        """
        liabilities = self.search("^Liabilities$")
        stockholders_equity = self.search("^StockholdersEquity$")
        years = liabilities.columns.to_list()
        dataframe = liabilities.reindex([("DebtCapitalization", "ratio")])

        for year in years:
            dataframe[year] = liabilities[year][0] / \
                (liabilities[year][0] + stockholders_equity[year][0])

        return dataframe.values[0] if as_list else dataframe


    def revenue(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates revenue

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the revenue
        """
        revenue = self.search(
            "^RevenueFromContractWithCustomerExcludingAssessedTax$"
            "|^Revenues$"
            "|^SalesRevenueNet$"
            "|RevenueFromContractWithCustomerIncludingAssessedTax$"
            # "|^SalesRevenueGoodsNet$"
            # "|^SalesRevenueServicesNet$"
        ).fillna(method="ffill").fillna(method="bfill").drop_duplicates()
        years = revenue.columns.to_list()
        dataframe = revenue.reindex([("Revenue", "USD")])

        for year in years:
            dataframe[year] = revenue[year][0]

        return dataframe.values[0] if as_list else dataframe


    def inventory_turnover(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates inventory tower = revenue / inventory net

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the inventory turnover
        """
        revenue = self.revenue()
        inventory = self.search("^InventoryNet$")
        years = revenue.columns.to_list()
        dataframe = revenue.reindex([("InventoryTurnover", "ratio")])

        for year in years:
            dataframe[year] = revenue[year][0] / inventory[year][0]

        return dataframe.values[0] if as_list else dataframe


    def cash_turnover(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates cash turnover = revenue / cash and cash equivalents
        at carrying value

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the cash turnover
        """
        revenue = self.revenue()
        cash = self.search("^CashAndCashEquivalentsAtCarryingValue$")
        years = revenue.columns.to_list()
        dataframe = revenue.reindex([("CashTurnover", "ratio")])

        for year in years:
            dataframe[year] = revenue[year][0] / cash[year][0]

        return dataframe.values[0] if as_list else dataframe


    def asset_turnover(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates asset turnover = revenue / assets

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the asset turnover
        """
        revenue = self.revenue()
        assets = self.search("^Assets$")
        years = revenue.columns.to_list()
        dataframe = revenue.reindex([("AssetTurnover", "ratio")])

        for year in years:
            dataframe[year] = revenue[year][0] / assets[year][0]

        return dataframe.values[0] if as_list else dataframe


    def current_asset_turnover(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates current asset turnover = revenue / current assets

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the current asset turnover
        """
        revenue = self.revenue()
        current_assets = self.search("^AssetsCurrent$")
        years = revenue.columns.to_list()
        dataframe = revenue.reindex([("CurrentAssetTurnover", "ratio")])

        for year in years:
            dataframe[year] = revenue[year][0] / current_assets[year][0]

        return dataframe.values[0] if as_list else dataframe


    def receivables_turnover(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates receivables turnover = revenue / account receivable

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the receivables turnover
        """
        revenue = self.revenue()
        accounts_receibale = self.search("^AccountsReceivableNetCurrent$")
        years = revenue.columns.to_list()
        dataframe = revenue.reindex([("ReceivablesTurnover", "ratio")])

        for year in years:
            dataframe[year] = revenue[year][0] / accounts_receibale[year][0]

        return dataframe.values[0] if as_list else dataframe


    def effective_tax_rate(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates effective tax rate = income tax / EBIT

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the effective tax rate
        """
        income_tax = self.search("^IncomeTaxExpenseBenefit$")
        ebit = self.ebit()
        years = income_tax.columns.to_list()
        dataframe = income_tax.reindex([("EffectiveTaxRate", "ratio")])

        for year in years:
            dataframe[year] = income_tax[year][0] / ebit[year][0]

        return dataframe.values[0] if as_list else dataframe


    def net_working_capital(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates net working capital = current assets - liabilities

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the effective tax rate
        """
        current_assets = self.search("^AssetsCurrent$")
        current_liabilities = self.search("^LiabilitiesCurrent$")
        years = current_assets.columns.to_list()
        dataframe = current_assets.reindex([("NetWorkingCapital", "USD")])

        for year in years:
            dataframe[year] = current_assets[year][0] - current_liabilities[year][0]

        return dataframe.values[0] if as_list else dataframe


    def net_working_capital_per_share(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates net working capital = current assets - liabilities

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the effective tax rate
        """
        net_working_capital = self.net_working_capital()
        shares = self.search("^CommonStockSharesOutstanding$")
        years = net_working_capital.columns.to_list()
        dataframe = net_working_capital.reindex([("NetWorkingCapitalPerShare", "USD")])

        for year in years:
            dataframe[year] = net_working_capital[year][0] / shares[year][0]

        return dataframe.values[0] if as_list else dataframe


    def net_income(self, as_list:bool=False) -> pd.DataFrame:
        """
        calculates net income

        Args:
            as_list (bool, optional): returns values as a list if True,
                as a dataframe otherwise. Defaults to False.

        Returns:
            pd.DataFrame: the net income
        """
        net_income = self.search("^NetIncomeLoss$")
        years = net_income.columns.to_list()
        dataframe = net_income.reindex([("NetIncome", "USD")])

        for year in years:
            dataframe[year] = net_income[year][0]

        return dataframe.values[0] if as_list else dataframe

######## Fundementals Task (FEB 10) #########

    # def price_to_earnings(self, as_list:bool=False) -> pd.DataFrame:
    #     """
    #     calculates price to earnings (stock price/earnings per share)

    #     Args:
    #         as_list (bool, optional): returns values as a list if True,
    #             as a dataframe otherwise. Defaults to False.

    #     Returns:
    #         pd.DataFrame: price to earnings
    #     """
    #     net_income_loss = self.search("^NetIncomeLoss$")
    #     common_shares_outstanding = self.search("^CommonSharesOutstanding$")
    #     years = net_income_loss.columns.to_list()
    #     dataframe = net_income_loss.reindex([("NetIncome", "USD")])

    #     for year in years:
    #         dataframe[year] = net_income[year][0]

    #     return dataframe.values[0] if as_list else dataframe


    # def piotroski_f_score(self, as_list:bool=False) -> pd.DataFrame:
    #     """
    #     calculates Piotroski F-Score

    #     Args:
    #         as_list (bool, optional): returns values as a list if True,
    #             as a dataframe otherwise. Defaults to False.

    #     Returns:
    #         pd.DataFrame: the Piotroski F-Score
    #     """
    #     return_on_assets = self.return_on_assets()
    #     net_cash = self.search("^NetCashProvidedByUsedInOperatingActivities$")
    #     net_income = self.net_income()
    #     gross_profit_t = self.search("^G")

    #     years = net_working_capital.columns.to_list()
    #     dataframe = net_working_capital.reindex([("NetWorkingCapitalPerShare", "USD")])

    #     for year in years:
    #         dataframe[year] = net_working_capital[year][0] / shares[year][0]

    #     return dataframe.values[0] if as_list else dataframe


class Form10K(Form):
    """
    Abstract Data Type for the SEC Form 10-K
    """
    @staticmethod
    def _format(dataframe:pd.DataFrame) -> pd.DataFrame:
        """
        adds a column designating which source column dataframe values came from

        Args:
            dataframe (pd.DataFrame): the raw content

        Returns:
            pd.DataFrame: the formatted content
        """
        dataframe = dataframe.pivot_table(
            index=["tag", "uom", "ddate", "fye"],
            columns="fy",
            values="value",
            aggfunc="max"
        )

        dataframe["monthday"] = dataframe.index.get_level_values("ddate").map(
            lambda d: "{:02d}{:02d}".format(d.month, d.day)
            )
        filtered = dataframe.loc[dataframe["monthday"] == dataframe.index.get_level_values("fye")]
        grouped = filtered.groupby(["tag", "uom"]).last()
        return grouped.drop("monthday", axis=1)



class Form10Q(Form):
    """
    Abstract Data Type for the SEC Form 10-Q
    """
    @staticmethod
    def _format(dataframe:pd.DataFrame) -> pd.DataFrame:
        """
        group source content into 10Q format

        Args:
            dataframe (pd.DataFrame): the raw content

        Returns:
            pd.DataFrame: the formatted content
        """
        dataframe = dataframe.pivot_table(
            index=["tag", "uom", "ddate"],
            columns=["fy", "fp"],
            values="value",
            aggfunc="min"
        )
        return dataframe.groupby(["tag", "uom"]).last()
