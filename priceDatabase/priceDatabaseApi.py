from .priceDatabaseManagment import *
from .priceGenerator import *

from fastapi import APIRouter
import json

priceDatabase_api = APIRouter(prefix='/priceDatabase', tags=['Price Database'])
price_database = priceDatabase(DatabaseName=r'./priceDatabase/PriceDatabase.db')


@priceDatabase_api.get('/getSpot')
def getSpotPrice(instrument: str):
    retprice = get_spot_price(instrument=instrument)
    return retprice


@priceDatabase_api.post('/generateCandleStick')
def generateCandleStick(instrument, startPrice: float, volatility: float, timeframe: str = '1Min'):
    global price_database

    ret = price_database.candle_price_generator(
        instrument=instrument, startPrice=startPrice, volatility=volatility, timeframe=timeframe)
    return ret


@priceDatabase_api.get('/getPrice')
def getPrice(instrument: str, timeframe: str = '1Min'):
    global price_database

    df = price_database.get_price(
        instrument=instrument, timeframe=timeframe)
    try:
        ret = df.copy()
        res = ret.to_json(orient="records")
        parsed = json.loads(res)
        return parsed
    except:
        return df


@priceDatabase_api.post('/generateHisPrice')
def generateHisPrice(instrument: str, startPrice: float, volatility: float, timeframe='1Min'):
    global price_database

    df = price_database.his_price_generator(instrument=instrument, startPrice=float(
        startPrice), volatility=volatility, timeframe=timeframe)
    try:
        ret = df.copy()
        res = ret.to_json(orient="records")
        parsed = json.loads(res)
        return parsed
    except:
        return df


@priceDatabase_api.get('/getDataByDate')
def getDataByDate(instrument: str, sdate, edate, timeframe: str = '1Min'):
    global price_database

    df = price_database.get_price_by_datetime(
        instrument=instrument, sdate=sdate, edate=edate, timeframe=timeframe)
    try:
        ret = df.copy()
        res = ret.to_json(orient="records")
        parsed = json.loads(res)
        return parsed
    except:
        return df


@priceDatabase_api.get('/getDataByN')
def getDataByN(instrument: str, n: int, timeframe: str = '1Min'):
    global price_database

    df = price_database.get_price_by_n(
        instrument=instrument, n=n, timeframe=timeframe)
    try:
        ret = df.copy()
        res = ret.to_json(orient="records")
        parsed = json.loads(res)
        return parsed
    except:
        return df


@priceDatabase_api.get('/getDataByLast')
def getDataByLast(instrument: str, n: int, timeframe: str = '1Min'):
    global price_database

    df = price_database.get_price_by_lastn(
        instrument=instrument, n=n, timeframe=timeframe)
    try:
        ret = df.copy()
        res = ret.to_json(orient="records")
        parsed = json.loads(res)
        return parsed
    except:
        return df


@priceDatabase_api.delete('/delete')
def deletePrice(instrument, timeframe: str = "1Min"):
    global price_database

    ret = price_database.delete_price(
        instrument=instrument, timeframe=timeframe)
    return ret


@priceDatabase_api.delete('/deleteByDatetime')
def deleteByDatetime(instrument, sdate, edate, timeframe: str = '1Min'):
    global price_database

    ret = price_database.delete_price_by_datetime(
        instrument=instrument, sdate=sdate, edate=edate, timeframe=timeframe)
    return ret


@priceDatabase_api.delete('/deleteByN')
def deleteByN(instrument: str, n: int, timeframe: str = '1Min'):
    global price_database

    ret = price_database.delete_price_by_n(
        instrument=instrument, n=n, timeframe=timeframe)
    return ret
