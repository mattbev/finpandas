"""
upload data files to AWS RDS database
"""

import csv
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from finpandas import Fundamentals

from update import update_dera_financials

data_path = Path(__file__).resolve().parent.parent.joinpath("data", "financials")

#pylint: disable=protected-access

def sub(instance:Fundamentals, folder:str):
    """
    upload a sub table

    Args:
        instance (Fundamentals): a Fundamentals instance with insert privilages
        folder (str): the name of the data folder to upload, i.e. "2018q3"
    """
    intermediate_start_time = datetime.now()
    print(f"inserting folder {folder} into sub.")

    table = pd.read_csv(data_path.joinpath(folder, "sub.txt"), sep="\t")
    table["folder"] = folder
    instance._commitdb("sub", table)
    intermediate_end_time = datetime.now()
    print(
        f"completed inserting folder {folder} into sub, "
        f"took: {intermediate_end_time-intermediate_start_time}"
    )


def tag(instance:Fundamentals, folder:str):
    """
    upload a tag table. Note this uses a different process than the
    other tables as this table breaks unique relational structure

    Args:
        instance (Fundamentals): a Fundamentals instance with insert privilages
        folder (str): the name of the data folder to upload, i.e. "2018q3"
    """
    intermediate_start_time = datetime.now()
    print(f"inserting folder {folder} into tag.")

    table = pd.read_csv(data_path.joinpath(folder, "tag.txt"), sep="\t")
    table["folder"] = folder
    conn = instance.engine.raw_connection()
    with conn.cursor() as cur:
        tag_command = (
            "INSERT INTO tag "
            "(tag, version, custom, abstract, datatype, iord, crdr, tlabel, doc, folder) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE tag=tag"
        )
        data = table.applymap(str).values.tolist()
        cur.executemany(tag_command, data)
    conn.commit()

    intermediate_end_time = datetime.now()
    print(
        f"completed inserting folder {folder} into tag, "
        f"took: {intermediate_end_time-intermediate_start_time}"
    )


def num(instance:Fundamentals, folder:str):
    """
    upload a num table

    Args:
        instance (Fundamentals): a Fundamentals instance with insert privilages
        folder (str): the name of the data folder to upload, i.e. "2018q3"
    """
    intermediate_start_time = datetime.now()
    print(f"inserting folder {folder} into num.")

    table = pd.read_csv(data_path.joinpath(folder, "num.txt"), sep="\t")
    table["folder"] = folder
    instance._commitdb("num", table)

    intermediate_end_time = datetime.now()
    print(
        f"completed inserting folder {folder} into num, "
        f"took: {intermediate_end_time-intermediate_start_time}"
    )


def pre(instance:Fundamentals, folder:str):
    """
    upload a pre table

    Args:
        instance (Fundamentals): a Fundamentals instance with insert privilages
        folder (str): the name of the data folder to upload, i.e. "2018q3"
    """
    intermediate_start_time = datetime.now()
    print(f"inserting folder {folder} into pre.")

    table = pd.read_csv(data_path.joinpath(folder, "pre.txt"), sep="\t")
    table["folder"] = folder
    instance._commitdb("pre", table)

    intermediate_end_time = datetime.now()
    print(
        f"completed inserting folder {folder} into pre, "
        f"took: {intermediate_end_time-intermediate_start_time}"
    )


def upload_dera_financials(instance:Fundamentals, folder:str, update_data:bool=True):
    """
    upload dera financials to the AWS MySQL database

    Args:
        instance (Fundamentals): a Fundamentals instance with insert privilages
        folder (str): the name of the data folder to upload, i.e. "2018q3"
        update_data (bool, optional): checks if local data is up to date. Defaults to True.
    """
    if update_data:
        print("updating data...")
        update_dera_financials()
        print("completed updated data.")

    print("processing {folder}...".format(folder=folder))

    start_time = datetime.now()

    max_int = sys.maxsize
    while True:
        try:
            csv.field_size_limit(max_int)
            break
        except OverflowError:
            max_int = max_int // 10

    sub(instance, folder)
    tag(instance, folder)
    num(instance, folder)
    pre(instance, folder)


    end_time = datetime.now()
    print(f"{folder} upload completed. Time elapsed: {end_time-start_time}")
    instance.dispose()


# if __name__ == "__main__":
    # instance = Fundamentals(username, password)
    # start = datetime.now()
    # upload_dera_financials(instance, "2020q3")
    # for folder in tqdm(next(os.walk("data"))[1]):
    #     main(instance, folder)
    #     print("x" * 30)
    # end = datetime.now()
    # print("Database population completed. Time elapsed: {t}".format(t=end-start))
