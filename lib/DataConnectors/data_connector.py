import json
import sqlite3
import time
import urllib.request

import pandas as pd

from data.data import API_KEY
from db.dbutils import check_ticker_exists, get_db, update_blacklisted, check_blacklisted


def get_data(url, delay=20):
    while True:
        df = json.loads(urllib.request.urlopen(url).read())
        if df.get("Note", 0) == 0:
            break
        time.sleep(20)
    return df


def grab_a_ticker(symbol="MSFT", apiKey=API_KEY):
    # Check if ticker already exists in the database
    if not check_ticker_exists(symbol) and not check_blacklisted(symbol):
        requestUrl = r"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=full&apikey={}"
        metaDataUrl = (
            r"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey={}"
        )
        data = get_data(requestUrl.format(symbol, apiKey))
        metaData = get_data(metaDataUrl.format(symbol, apiKey))
        df = pd.DataFrame(
            pd.DataFrame(data.get("Time Series (Daily)")).transpose()["4. close"]
        ).reset_index()

        df.columns = ["Date", "Price"]
        df["Symbol"] = data["Meta Data"]["2. Symbol"]
        if len(metaData["bestMatches"]) > 0:
            met_df = (
                pd.DataFrame(metaData["bestMatches"][0], index=[0])[
                    ["1. symbol", "2. name", "3. type", "4. region"]
                ]
                .reset_index()
                .drop(["index"], axis=1)
            )
            met_df.columns = ["Symbol", "Name", "Type", "Region"]
        else:
            print(metaData.keys())
            met_df = pd.DataFrame()

        try:
            assert met_df.iloc[0, :].Symbol == df.iloc[0, :].Symbol
            df.to_sql("time_series", con=get_db(), if_exists="append", index=False)
            met_df.to_sql("stock_meta_data", con=get_db(), if_exists="append", index=False)
        except AssertionError as e:
            print("'Couldn't get it right with assertion error: {}".format(str(e)))
            update_blacklisted(symbol)
        except Exception as e:
            print(str(e))
            update_blacklisted(symbol)
    else:
        print("Symbol {} already exists.".format(symbol))
