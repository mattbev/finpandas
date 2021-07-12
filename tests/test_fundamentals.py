import unittest
from concurrencytest import ConcurrentTestSuite, fork_for_tests

from finpandas import dispose, fundamentals
from finpandas.utils import count_object_methods

###########################################################################
######################### Basic Operational Tests #########################
###########################################################################

class TestFundamentalsOperations(unittest.TestCase):
    # # ~~~~~~~~~~~ get_profile_by_cik ~~~~~~~~~~ #
    # def test_get_profile_by_cik_runs(self):
    #     fundamentals.get_profile_by_cik(320193)


    # # ~~~~~~~~~ get_profile_by_ticker ~~~~~~~~~ #
    # def test_get_profile_by_ticker_runs(self):
    #     fundamentals.get_profile_by_ticker("fb")


    # # ~~~~~~~~~~ get_profile_by_title ~~~~~~~~~ #
    # def test_get_profile_by_title_runs(self):
    #     fundamentals.get_profile_by_title("Apple*")


    # ~~~~~~~~~~~~~~~~~ query ~~~~~~~~~~~~~~~~~ #
    def test_query_runs(self):
        pass


    # ~~~~~~~~~~~~~~~ query_10k ~~~~~~~~~~~~~~~ #
    def test_query_10k_runs_single_year(self):
        fundamentals.ten_k("aapl", 2018)

    def test_query_10k_runs_multiple_years(self):
        fundamentals.ten_k("aapl", [2018, 2019])


    # ~~~~~~~~~~~~~~~ query_10q ~~~~~~~~~~~~~~~ #
    def test_query_10q_runs_single_year(self):
        fundamentals.ten_q("googl", 2018)

    def test_query_10q_runs_multiple_years(self):
        fundamentals.ten_q("googl", [2018, 2019])

    def test_query_10q_runs_single_period(self):
        fundamentals.ten_q("ibm", (2016, "q1"))

    def test_query_10q_runs_multiple_periods(self):
        fundamentals.ten_q("ibm", [(2016, "q2"), (2017, "q3")])


###########################################################################
############################## Validity Tests #############################
###########################################################################
# TODO


if __name__ == '__main__':
    operations_suite = unittest.TestLoader().loadTestsFromTestCase(TestFundamentalsOperations)
    concurrent_operations_suite = ConcurrentTestSuite(
        operations_suite, 
        fork_for_tests(count_object_methods(TestFundamentalsOperations))
    )
    runner = unittest.TextTestRunner()
    runner.run(concurrent_operations_suite)

    dispose()