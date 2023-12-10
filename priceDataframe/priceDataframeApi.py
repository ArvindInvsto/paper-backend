from .priceDataframe import *
from fastapi import APIRouter
from pydantic import BaseModel
import json

priceDataframe_api = APIRouter(
    prefix='/priceDataframe', tags=['Price Dataframe'])


@priceDataframe_api.get('/getHisData')
def getHisData(tickers="SBIN.NS",
               start: str = "",
               end: str = "",
               interval="1d",
               period="max"):
    start = None if len(start) < 1 else start
    end = None if len(end) < 1 else end

    df = get_his_data(tickers=tickers, start=start,
                      end=end, period=period, interval=interval)
    ret = df.copy()
    res = ret.to_json(orient="index")
    parsed = json.loads(res)

    return parsed
