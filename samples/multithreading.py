import time

from finpandas import fundamentals, dispose
from finpandas.utils import Jobs


def main():

    # forms that we want
    companies = ['aapl', 'msft', 'fb']
    years = [2017, 2018, 2019]

    # multithreading
    start = time.time()
    jobs = Jobs()
    for company in companies:
        jobs.add_job(fundamentals.ten_k, company, years)
    par_results = jobs.execute()
    print('parallel:', time.time() - start)

    # sequential
    # start = time.time()
    # seq_results = []
    # for company in companies:
    #     seq_results.append(fundamentals.ten_k(company, years))
    # print('sequential:', time.time() - start)

    # manipulate them
    for r in par_results:
        print(r.return_on_assets())


if __name__ == '__main__':
    main()
    dispose()