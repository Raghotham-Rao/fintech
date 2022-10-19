import requests
import pandas as pd
import json
from datetime import datetime, timedelta


class NSEDataLoader:
    headers = {
        "user-agent": "Custom",
    }

    @staticmethod
    def load_data(symbol:str, from_date:str=None, to_date:str=datetime.now().date()):
        """
        load historical data of a script from NSE.

        Parameters
        ----------
        symbol: str
                The script short-code/symbol.
        from_date: str, optional
                The date from which historical data is to be retrieved.
                The expected format is `yyyy-mm-dd`.
                By default it is `None`.
                If not specified, data for the range (to_date - 90 days, to_date) will be retrieved.
        to_date: str, optional
                The date till which historical data is to be retrieved.
                The expected format is `yyyy-mm-dd`.
                The default value is the current date.

        Returns
        -------
        A pandas dataframe containing the required historical data of the stock.
        """
        params = {
            "symbol": "INFY",
            "from": "01-10-2021",
            "to": "18-10-2022"
        }

    @staticmethod
    def load_x_days_data(from_date, x):
        ...

    @staticmethod
    def load_last_x_days_data(x):
        ...

base_url = 'https://www.nseindia.com/api/historical/cm/equity'