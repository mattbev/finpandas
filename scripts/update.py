"""
update data files from the SEC
"""

import datetime
import io
import json
import time
import zipfile
from pathlib import Path

import requests

#pylint: disable=invalid-name

def update_company_profiles():
    """
    update company ticker, cik, title mappings from the SEC
    """
    # url = "https://www.sec.gov/include/ticker.txt" # for the text version without company title
    url = "https://www.sec.gov/files/company_tickers.json"

    start = time.time()

    r = requests.get(url)
    json_file = r.json()

    corrections = {
        "BFA" : {
                "cik_str": 14693,
                "ticker": "BF-A",
                "title": "BROWN FORMAN CORP"
        },
    }
    insertions = {
        "BF-B": {
            "cik_str": 14693,
            "ticker": "BF-B",
            "title": "BROWN FORMAN CORP"
        },
    }
    json_file.update(insertions)

    ticker_json = {}
    cik_json = {}
    title_json = {}
    for idx in json_file:
        row = json_file[idx]
        ticker_key = row["ticker"]
        if ticker_key in corrections:
            row = corrections[ticker_key]
            ticker_key = row["ticker"]
        cik_key = row["cik_str"]
        title_key = row["title"]
        ticker_json[ticker_key] = row
        cik_json[cik_key] = row
        title_json[title_key] = row

    with open('blacktip/utils/ticker.json', 'w', encoding='utf-8') as f:
        json.dump(ticker_json, f, ensure_ascii=False, indent=4)

    with open('blacktip/utils/cik.json', 'w', encoding='utf-8') as f:
        json.dump(cik_json, f, ensure_ascii=False, indent=4)

    with open('blacktip/utils/title.json', 'w', encoding='utf-8') as f:
        json.dump(title_json, f, ensure_ascii=False, indent=4)

    end = time.time()
    print("\nUpdated company profiles.")
    print("time elapsed:", end-start)


def update_dera_financials():
    """
    update dera financial folders from the SEC
    """
    data_path = Path(__file__).resolve().parent.parent.joinpath("data", "financials")

    start = time.time()

    quarters = ["q1", "q2", "q3", "q4"]
    years = [str(i) for i in range(2009, datetime.datetime.now().year+1)]
    for year in years:
        for quarter in quarters:
            period = year+quarter
            period_path = data_path.joinpath(period)
            if period_path.exists():
                print("skipped period:", period)
                continue
            url = f"https://www.sec.gov/files/dera/data/financial-statement-data-sets/{period}.zip"
            r = requests.get(url)
            if r.status_code==200:
                z = zipfile.ZipFile(io.BytesIO(r.content))
                period_path.mkdir(parents=True, exist_ok=False)
                z.extractall(period_path)
                print("extracted period:", period)
            else:
                print("error getting period:", period)

    end = time.time()
    print("\nUpdated company profiles.")
    print("time elapsed:", end-start)

if __name__ == "__main__":
    update_company_profiles()
    update_dera_financials()
