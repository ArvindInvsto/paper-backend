import yfinance as yf


def get_his_data(tickers, start=None, end=None, period="max", interval="1d"):
    df = yf.download(tickers, start=start, end=end,
                     period=period, interval=interval)
    return df
