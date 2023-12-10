from .priceGenerator import candleGenerator, hisPriceGenerator

import pytz
import sqlite3
import pandas as pd
from datetime import datetime


class priceDatabase:
    def __init__(self, DatabaseName: str) -> None:
        '''
        DatabaseName(str): Name of the database (e.g. testDatabase.db)
        '''

        try:
            # Connect to the DB and create a cursor
            self.sqliteConnection = sqlite3.connect(
                DatabaseName, check_same_thread=False)
            self.cursor = self.sqliteConnection.cursor()

        except Exception as e:
            exit(print(f'{e}: while connecting to the {DatabaseName}!'))

    def get_price(self, instrument, timeframe='1Min'):
        try:
            query = f"select * from {instrument} where Timeframe='{timeframe}'"
            df = pd.read_sql(query, con=self.sqliteConnection)
            if len(df) == 0:
                return {'Error': 'No data found, try to generate price!'}
            return df
        except Exception as e:
            if 'no such table' in str(e):
                return {'Error': "Please generate price first!"}
            return {"Error": f"{e}"}

    def his_price_generator(self, instrument, startPrice, volatility, timeframe):
        df = hisPriceGenerator(instrument=instrument, startPrice=startPrice,
                               volatility=volatility, timeframe=timeframe)
        df.to_sql(name=instrument, con=self.sqliteConnection,
                  if_exists='append')

        df = self.get_price(instrument=instrument, timeframe=timeframe)
        return df

    def candle_price_generator(self, instrument, startPrice, volatility, timeframe='1Min'):
        ret = candleGenerator(
            instrument=instrument, startPrice=startPrice, volatility=volatility, num=1)
        ret[0]['Timeframe'] = timeframe
        
        utcTimezone=pytz.timezone('UTC')
        ret[0]['Datetime'] = datetime.now(utcTimezone).strftime("%d/%m/%Y %H:%M")
        
        df = pd.DataFrame(ret)
        df.index = df['Datetime']
        df.drop(['Datetime'], axis=1, inplace=True)

        try:
            df.to_sql(name=instrument, con=self.sqliteConnection,
                      if_exists='append')
            return ret
        except Exception as e:
            return {"Error": f"{e}"}

    def get_price_by_datetime(self, instrument, sdate, edate, timeframe='1m'):
        try:
            query = f"Select * from {instrument} where (Datetime between '{sdate}' and '{edate}') and timeframe='{timeframe}'"
            df = pd.read_sql(query, con=self.sqliteConnection)
            if len(df) == 0:
                return {'Error': 'No data found, try to generate price!'}
            return df
        except Exception as e:
            return {"Error": f"{e}, while fetching data!"}

    def get_price_by_n(self, instrument, n, timeframe='1Min'):
        try:
            query = f"Select * from {instrument}  where timeframe='{timeframe}' limit {n}"
            df = pd.read_sql(query, con=self.sqliteConnection)
            if len(df) == 0:
                return {'Error': 'No data found, try to generate price!'}
            return df
        except Exception as e:
            return {"Error": f"{e}, while fetching data!"}

    def get_price_by_lastn(self, instrument, n, timeframe='1Min'):
        try:
            query = f"Select * from {instrument}  where timeframe='{timeframe}' ORDER BY Datetime DESC limit {n}"
            df = pd.read_sql(query, con=self.sqliteConnection)
            if len(df) == 0:
                return {'Error': 'No data found, try to generate price!'}
            return df
        except Exception as e:
            return {"Error": f"{e}, while fetching data!"}

    def delete_price(self, instrument, timeframe: str = "1Min"):
        try:
            query = f"Delete from {instrument} where timeframe='{timeframe}'"
            self.cursor.execute(query)
            self.sqliteConnection.commit()
            return {"Success": "Deleted Successfully"}
        except Exception as e:
            return {"Error": f"{e}"}

    def delete_price_by_datetime(self, instrument, sdate, edate, timeframe: str = "1Min"):
        try:
            query = f"Delete from {instrument} where (Datetime between '{sdate}' and '{edate}') and timeframe='{timeframe}'"
            self.cursor.execute(query)
            self.sqliteConnection.commit()
            return {"Success": "Deleted successfully"}
        except Exception as e:
            return {"Error": f"{e}"}

    def delete_price_by_n(self, instrument, n, timeframe='1m'):
        try:
            query = f"Delete from {instrument} where  rowid in (Select rowid  from {instrument}  where timeframe='{timeframe}' limit {n})"
            self.cursor.execute(query)
            self.sqliteConnection.commit()
            return {"Success": "Deleted Successfully"}
        except Exception as e:
            return {"Error": f"{e}"}
