 import requests
import time
from datetime import datetime
from getExpiry import Expiry

# Generate CandleStick
def generateCandleSticke(instrument, startPrice, volatility, timeframe):
    '''
    http://3.143.6.63:8000/priceDatabase/generateCandleStick?instrument=SBIN&startPrice=500&volatility=0.00001&timeframe=1Min
    '''




    # BaseUrls
    baseUrl = r"http://3.143.6.63:8000/"

    # Price
    priceDatabase = baseUrl+'priceDatabase/'

    extendedUrl = priceDatabase+'generateCandleStick'
    params = locals()
    ret = requests.post(extendedUrl, params=params)
    return ret.json()


def deletePrice(instrument, timeframe):
    '''
    http://3.143.6.63:8000/priceDatabase/delete?instrument=SBIN&timeframe=1Min
    '''

    # BaseUrls
    baseUrl = r"http://3.143.6.63:8000/"

    # Price
    priceDatabase = baseUrl+'priceDatabase/'

    extendedUrl = priceDatabase+'delete'
    params = locals()
    ret = requests.delete(extendedUrl, params=params)
    return ret.json()

while True:
    nowtime=datetime.now().strftime('%H:%M')

    strike={'17750':160, '17700': 140, '17650': 120, '17600': 100, '17550': 80,
             '17500': 60, '17450': 40, '17400': 35, '17350':30, '17300':25, '17250':20}
    expiry=Expiry()
    expiryDate=expiry.getWeeklyExpiryDate(numWeeksPlus=0)

    if nowtime >= '00:00' and nowtime < '23:55':
        for key in strike.keys():
            instrument='NIFTY'+expiryDate+'CE'+key
            callOptions=(generateCandleSticke(instrument=instrument, startPrice=strike[key], volatility=0.03, timeframe='1Min'))
            print(callOptions)

    if nowtime == '23:55':
        for key in strike.keys():
            instrument='NIFTY'+expiryDate+'CE'+key
            print(deletePrice(instrument=instrument, timeframe='1Min'))
    
    time.sleep(60)
