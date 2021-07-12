"""
finpandas base module.
"""

from dataclasses import dataclass

import pandas as pd
import sqlalchemy


@dataclass
class DatabaseConnection:
    """
    Establish a connection with the database.

    Args:
        username (str): your username
        password (str): your password
    """

    database: str
    username: str = 'finpandas'
    password: str = None
    _host: str = "database-blacktip.cpeql2xeyjqq.us-east-2.rds.amazonaws.com"
    _port: int = 3306


    def __post_init__(self):
        self.engine = self._create_engine()


    def query(self, command:str):# -> sqlalchemy.engine.Result:
        """
        query information directly from the database

        Args:
            command (str): the string mySQL command to execute

        Returns:
            sqlalchemy.engine.Result: the results of the query
        """
        with self.engine.connect() as connection:
            return connection.execute(command)


    def dispose(self):
        """
        closes the database connection
        """
        self.engine.dispose()



    ########## Private Functions ##########


    def _commitdb(self, table_name:str, dataframe:pd.DataFrame):
        """
        commit to the database

        Args:
            table_name (str): the name of the table to commit to
            dataframe (pd.DataFrame): the data to commit to the table
        """
        dataframe.to_sql(table_name, self.engine, index=False, if_exists="append")


    def _create_engine(self) -> sqlalchemy.engine.Engine:
        """
        establish connection to MySQL database

        Returns:
            sqlalchemy.engine.Engine: SQLAlchemy engine instance
        """
        if self.password is not None:
            url = f'mysql+pymysql://{self.username}:{self.password}@{self._host}:{self._port}/{self.database}'
        else:
            url = f'mysql+pymysql://{self.username}@{self._host}:{self._port}/{self.database}'
        engine = sqlalchemy.create_engine(url)
        return engine
